'''
MAIN

Notes
- Monitors and reacts to the user interface via the interface.db database
- Checks spectral sensor via the hematuria.json database
- Checks supply and waste weight sensors
- Controls irrigation manually (user input) or automatically (PID feedback)
- Checks and initiates alerts
- Updates system.db database
- Resets device

Documentation
- PID feedback guide: https://simple-pid.readthedocs.io/en/latest/index.html
- PID tuning guide: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=9013

'''

import os
import time
import numpy as np
from datetime import datetime
import pytz
from simple_pid import PID
import board
from sklearn.linear_model import LinearRegression

from data import *
from timer import Timer

from components.button import Button
from components.light import Light
from components.linear_actuator import LinearActuator
from components.speaker import Speaker
# from components.spectral_sensor import SpectralSensor # run separately
from components.weight_sensor import WeightSensor


# script parameters
DEMO = True # for showcase demoing
VERBOSE = True # for debugging

if DEMO:
    retraction_count = 0 # FOR DEMO

# system parameters
# INFLOW_ADJUSTMENT_TIME = 0.005 # sec
INFLOW_ADJUSTMENT_TIME = 0.05 # sec # FOR DEMO

WEIGHT_CALIBRATION_REPLICATES = 15
WEIGHT_REPLICATES = 60
WEIGHT_OUTLIERS = 20
FLOW_RATE_REPLICATES = 60 # number of weight measurements to use for each rate calculation

SUPPLY_DENSITY = 1.0 # g/mL
WASTE_DENSITY = 1.0 # g/mL

# PID parameters
Kp = -0.15
Ki = 0
Kd = 0.05

INFLOW_LEVEL_ADJUST_TIME_LIMIT = 0.05 # +/- maximum adjustment time (seconds) in extension and retraction
HEMATURIA_SETPOINT = 0.5 # percent blood concentration

# alert parameters (ordered by prescedence)
ALERT_CAUTION_SOUND = 'sound/echo.mp3'
ALERT_CRITICAL_SOUND = 'sound/alarm.mp3'

ALERT_NORMAL_STATUS = 'NORMAL'
ALERT_NORMAL_MESSAGE = "System and patient normal."

ALERT_STARTUP_STATUS = 'SETUP'
ALERT_STARTUP_MESSAGE = 'System starting.'

ALERT_SUPPLY_LOW_PERCENT = 10
ALERT_SUPPLY_LOW_LEVEL = 'CAUTION' # if changing, adjust order of alert conditions below
ALERT_SUPPLY_LOW_MESSAGE = f'Supply bag volume <{ALERT_SUPPLY_LOW_PERCENT}%.'

ALERT_WASTE_HIGH_PERCENT = 90
ALERT_WASTE_HIGH_LEVEL = 'CAUTION' # if changing, adjust order of alert conditions below
ALERT_WASTE_HIGH_MESSAGE = f'Waste bag volume >{ALERT_WASTE_HIGH_PERCENT}%.'

ALERT_SUPPLY_FLOW_LOW_RATE = 1 # mL/min
ALERT_SUPPLY_FLOW_LOW_TIME = 5 # min
ALERT_SUPPLY_FLOW_LOW_LEVEL = 'CRITICAL' # if changing, adjust order of alert conditions below
ALERT_SUPPLY_FLOW_LOW_MESSAGE = f'Supply inflow rate <{ALERT_SUPPLY_FLOW_LOW_RATE} mL/min for >{ALERT_SUPPLY_FLOW_LOW_TIME} min.'

ALERT_SUPPLY_FLOW_HIGH_RATE = 200 # mL/min
ALERT_SUPPLY_FLOW_HIGH_TIME = 2 # min
ALERT_SUPPLY_FLOW_HIGH_LEVEL = 'CAUTION' # if changing, adjust order of alert conditions below
ALERT_SUPPLY_FLOW_HIGH_MESSAGE = f'Supply inflow rate >{ALERT_SUPPLY_FLOW_HIGH_RATE} mL/min for >{ALERT_SUPPLY_FLOW_HIGH_TIME} min.'

ALERT_WASTE_FLOW_LOW_RATE = 1 # mL/min
ALERT_WASTE_FLOW_LOW_TIME = 5 # min
ALERT_WASTE_FLOW_LOW_LEVEL = 'CRITICAL' # if changing, adjust order of alert conditions below
ALERT_WASTE_FLOW_LOW_MESSAGE = f'Waste outflow rate <{ALERT_WASTE_FLOW_LOW_RATE} mL/min for >{ALERT_WASTE_FLOW_LOW_TIME} min.'

ALERT_WASTE_FLOW_HIGH_RATE = 200 # mL/min
ALERT_WASTE_FLOW_HIGH_TIME = 2 # min
ALERT_WASTE_FLOW_HIGH_LEVEL = 'CAUTION' # if changing, adjust order of alert conditions below
ALERT_WASTE_FLOW_HIGH_MESSAGE = f'Waste outflow rate >{ALERT_WASTE_FLOW_HIGH_RATE} mL/min for >{ALERT_WASTE_FLOW_HIGH_TIME} min.'

ALERT_FLOW_DISCREPANCY_RATE = 20 # mL/min
ALERT_FLOW_DISCREPANCY_TIME = 10 # min
ALERT_FLOW_DISCREPANCY_LEVEL = 'CRITICAL' # if changing, adjust order of alert conditions below
ALERT_FLOW_DISCREPANCY_MESSAGE = f'Inflow rate greater than outflow rate by >{ALERT_FLOW_DISCREPANCY_RATE} mL/min for >{ALERT_FLOW_DISCREPANCY_TIME} min.'

ALERT_HEMATURIA_SEVERITY = 75 # hematuria severity level: clear (0-24), mild (25-49), moderate (50-74), severe (75-99)
ALERT_HEMATURIA_TIME = 10 # min
ALERT_HEMATURIA_LEVEL = 'CRITICAL' # if changing, adjust order of alert conditions below
ALERT_HEMATURIA_MESSAGE = f'Severe hematuria measured for >{ALERT_HEMATURIA_TIME} min.'

ALERT_EMERGENCY_BUTTON_LEVEL = 'CRITICAL' # if changing, adjust order of alert conditions below
ALERT_EMERGENCY_BUTTON_MESSAGE = 'Emergency button pressed; inflow stopped.'


# main loop
def main():

    # instantiate components, PID, and linear regression
    light = Light(red_pin=8, green_pin=7, blue_pin=1, verbose=VERBOSE)
    linear_actuator = LinearActuator(en_pin=13, in1_pin=19, in2_pin=26, freq=1000, verbose=VERBOSE)
    speaker = Speaker(verbose=VERBOSE)
    # spectral_sensor = SpectralSensor(led_pin=4, use_led=True, sensor_type='VIS', max=48000) # not directly used for measurements in main script
    supply_weight_sensor = WeightSensor(pdsck_pin=18, dout_pin=23, offset=1, scale=1, verbose=VERBOSE)
    waste_weight_sensor = WeightSensor(pdsck_pin=14, dout_pin=15, offset=1, scale=1, verbose=VERBOSE)
    emergency_button = Button(pin=10, verbose=VERBOSE)

    pid = PID(Kp, Ki, Kd, setpoint=HEMATURIA_SETPOINT, output_limits=(-1*INFLOW_LEVEL_ADJUST_TIME_LIMIT, INFLOW_LEVEL_ADJUST_TIME_LIMIT))
    regression = LinearRegression()


    # check if reset
    reset = False
    for file in ['system', 'interface', 'patient', 'hematuria']:
        if not exists_data(file=file):
            reset = True
            break

    if VERBOSE:
        print('reset = {reset}')
    
    # initialize new data if reset
    if reset == True:
        light.color(color = 'yellow')
        for file in ['system', 'interface', 'patient', 'hematuria']:
            delete_data(file=file)
            create_data(file=file)
    else:
        light.color(color='green')
    

    # get stored system data from database and assign to variables
    system_data = get_data(key='all', file='system')

    _ = system_data['hematuria_level'] # not necessary
    _ = system_data['hematuria_percent'] # not necessary

    _ = system_data['supply_percent'] # not necessary
    _ = system_data['supply_volume'] # not necessary
    _ = system_data['supply_time'] # not necessary
    _ = system_data['supply_rate'] # not necessary

    _ = system_data['waste_percent'] # not necessary
    _ = system_data['waste_volume'] # not necessary
    _ = system_data['waste_time'] # not necessary
    _ = system_data['waste_rate'] # not necessary

    _ = system_data['status_level'] # not necessary
    _ = system_data['status_message'] # not necessary

    _ = system_data['active_time'] # not necessary
    _ = system_data['current_date'] # not necessary
    _ = system_data['current_time'] # not necessary

    supply_volume_total = system_data['supply_volume_total']
    supply_volume_gross = system_data['supply_volume_gross']
    supply_replace_count = system_data['supply_replace_count']

    waste_volume_total = system_data['waste_volume_total']
    waste_volume_gross = system_data['waste_volume_gross']
    waste_replace_count = system_data['waste_replace_count']

    _ = system_data['automatic'] # not necessary
    _ = system_data['inflow_level'] # not necessary

    _ = system_data['mute'] # not necessary


    # get stored user interface data from database and assign to variables
    interface_data = get_data(key='all', file='interface')

    supply_replace_volume = interface_data['supply_replace_volume']
    supply_replace_count_removed = interface_data['supply_replace_count_removed']
    supply_replace_count_added = interface_data['supply_replace_count_added']
    
    waste_replace_volume = interface_data['waste_replace_volume']
    waste_replace_count_removed = interface_data['waste_replace_count_removed']
    waste_replace_count_added = interface_data['waste_replace_count_added']

    automatic = interface_data['automatic']
    inflow_level = interface_data['inflow_level']

    mute_count = interface_data['mute_count']

    _ = interface_data['setup'] # not necessary
    _ = interface_data['reset'] # not necessary
    
    # ensure consistency between databases
    supply_volume_total = supply_replace_volume
    waste_volume_total = waste_replace_volume


    # lists for averaging volumes
    supply_scans = []
    waste_scans = []

    # lists for calculating flow rates
    supply_volumes = []
    supply_volume_times = []
    waste_volumes = []
    waste_volume_times = []

    # additional variables for checking alert conditions
    alert_supply_low = False

    alert_waste_high = False

    alert_supply_flow_low = False
    alert_supply_flow_low_timer = Timer()

    alert_supply_flow_high = False
    alert_supply_flow_high_timer = Timer()

    alert_waste_flow_low = False
    alert_waste_flow_low_timer = Timer()

    alert_waste_flow_high = False
    alert_waste_flow_high_timer = Timer()

    alert_flow_discrepancy = False
    alert_flow_discrepancy_timer = Timer()

    alert_hematuria = False
    alert_hematuria_timer = Timer()

    alert_emergency_button = False
    alert_emergency = False

    # perform reset if reset
    if reset == True:

        # wait for patient info update (NOT NECESSARY, can be removed)
        while True:
            sex = get_data(key='sex', file='patient')
            if sex in ['M', 'F']:
                break
            time.sleep(0.01)

        # wait for replaced supply bag
        while True:
            val = get_data(key='supply_replace_count_removed', file='interface')
            if  val > supply_replace_count_removed:
                supply_replace_count_removed = val
                supply_weight_sensor.zero(replicates=WEIGHT_CALIBRATION_REPLICATES) # zero weight sensor
                break
            time.sleep(0.01)
        
        while True:
            val = get_data(key='supply_replace_count_added', file='interface')
            if val > supply_replace_count_added:
                time.sleep(0.4)
                supply_replace_count_added = val
                supply_replace_volume = get_data(key='supply_replace_volume', file='interface')
                if VERBOSE:
                    print(f'supply_replace_volume = {supply_replace_volume}')
                
                if DEMO:
                    supply_replace_volume = 1000 # FOR DEMO

                supply_weight_sensor.calibrate(known_mass=supply_replace_volume, replicates=WEIGHT_CALIBRATION_REPLICATES) # calibrate weight sensor with known mass
                supply_volume_total = supply_replace_volume # update
                supply_replace_count += 1 # update
                break
            time.sleep(0.01)
        
        # wait for replaced waste bag
        while True:
            val = get_data(key='waste_replace_count_removed', file='interface')
            if val > waste_replace_count_removed:
                waste_replace_count_removed = val
                waste_weight_sensor.zero(replicates=WEIGHT_CALIBRATION_REPLICATES) # zero weight sensor
                break
            time.sleep(0.01)
        
        while True:
            val = get_data(key='waste_replace_count_added', file='interface')
            if  val > waste_replace_count_added:
                time.sleep(0.4)
                waste_replace_count_added = val
                waste_replace_volume = get_data(key='waste_replace_volume', file='interface')
                if waste_replace_volume == 1000:
                    known_mass = 50
                elif waste_replace_volume == 2000:
                    known_mass = 75
                elif waste_replace_volume == 3000:
                    known_mass = 100
                
                if DEMO:
                    known_mass = 1000 # FOR DEMO
                    waste_replace_volume = 2000 # FOR DEMO
                
                if VERBOSE:
                    print(f'waste_replace_volume = {waste_replace_volume}')
                waste_weight_sensor.calibrate(known_mass=known_mass, replicates=WEIGHT_CALIBRATION_REPLICATES) # calibrate weight sensor with known mass
                waste_volume_total = waste_replace_volume # update
                waste_replace_count += 1 # update
                break
            time.sleep(0.01)

        # wait for replaced tubing (setup)
        s = time.time()
        while True:
            setup = get_data(key='setup', file='interface')
            if setup == True:
                linear_actuator.extend(duty_cycle=100, duration=min(4, time.time()-s+1)) # fully extend actuator
                break
            if ((time.time()-s) < 6):
                linear_actuator.retract(duty_cycle=100, duration=INFLOW_ADJUSTMENT_TIME) # retract actuator
            time.sleep(0.01)

        reset = False
    

    # get stored patient data from database and assign to variables
    patient_data = get_data(key='all', file='patient')
    
    _ = patient_data['firstname'] # not necessary (add back for alert SMS texting)
    _ = patient_data['lastname'] # not necessary (add back for alert SMS texting)
    _ = patient_data['MRN'] # not necessary (add back for alert SMS texting)
    _ = patient_data['DOB'] # not necessary (add back for alert SMS texting)
    _ = patient_data['sex'] # not necessary (add back for alert SMS texting)
    _ = patient_data['contact_A'] # not necessary (add back for alert SMS texting)
    _ = patient_data['contact_B'] # not necessary (add back for alert SMS texting)

    start_date = patient_data['start_date']
    start_time = patient_data['start_time']


    # begin normal operation
    iteration = 1 # number of entries added to system database
    while True:
        if VERBOSE:
            print(f'iteration = {iteration}')


        # check emergency button
        if iteration > FLOW_RATE_REPLICATES + WEIGHT_REPLICATES:
            if emergency_button.pressed() == True: # button pressed
                while True:
                    if emergency_button.pressed() == False: # button released
                        alert_emergency_button = not alert_emergency_button
                        if alert_emergency_button == False:
                            alert_emergency = False
                        break
                    time.sleep(0.01)
    

        # get and check user interface data from database
        # supply_replace_volume, supply_replace_count_removed, supply_replace_count_added
        val = get_data(key='supply_replace_count_removed', file='interface')
        if  val > supply_replace_count_removed:
            supply_replace_count_removed = val
            supply_weight_sensor.zero(replicates=WEIGHT_CALIBRATION_REPLICATES) # zero weight sensor

        val = get_data(key='supply_replace_count_added', file='interface')
        if val > supply_replace_count_added:
            supply_replace_count_added = val
            time.sleep(0.4)
            supply_replace_volume = get_data(key='supply_replace_volume', file='interface')
            if VERBOSE:
                print(f'supply_replace_volume = {supply_replace_volume}')

            if DEMO:
                supply_replace_volume = 1000 # FOR DEMO
            
            supply_weight_sensor.calibrate(known_mass=supply_replace_volume, replicates=WEIGHT_CALIBRATION_REPLICATES) # calibrate weight sensor with known mass
            supply_volume_gross +=  supply_volume_total - supply_volume # update
            supply_volume_total = supply_replace_volume # update
            supply_replace_count += 1 # update
            alert_supply_low = False

        # waste_replace_volume, waste_replace_count_removed, waste_replace_count_added
        val = get_data(key='waste_replace_count_removed', file='interface')
        if  val > waste_replace_count_removed:
            waste_replace_count_removed = val
            waste_weight_sensor.zero(replicates=WEIGHT_CALIBRATION_REPLICATES) # zero weight sensor'

        val = get_data(key='waste_replace_count_added', file='interface')
        if val > waste_replace_count_added:
            waste_replace_count_added = val
            time.sleep(0.4)
            waste_replace_volume = get_data(key='waste_replace_volume', file='interface')
            if waste_replace_volume == 1000:
                known_mass = 50
            elif waste_replace_volume == 2000:
                known_mass = 75
            elif waste_replace_volume == 3000:
                known_mass = 100
            
            if DEMO:
                known_mass = 1000 # FOR DEMO
                waste_replace_volume = 2000 # FOR DEMO

            if VERBOSE:
                print(f'waste_replace_volume = {waste_replace_volume}')
            waste_weight_sensor.calibrate(known_mass=known_mass, replicates=WEIGHT_CALIBRATION_REPLICATES) # calibrate weight sensor with known mass
            waste_volume_gross += waste_volume # update
            waste_volume_total = waste_replace_volume # update
            waste_replace_count += 1 # update
            alert_waste_high = False
            
        # automatic, inflow_level
        automatic = get_data(key='automatic', file='interface')
        val = get_data(key='inflow_level', file='interface')
        if val > inflow_level:
            inflow_level_adjust = 1
            inflow_level += 1
            if VERBOSE:
                print(f'inflow_level_adjust = {inflow_level_adjust}')
        elif val < inflow_level:
            inflow_level_adjust = -1
            inflow_level -= 1
            if VERBOSE:
                print(f'inflow_level_adjust = {inflow_level_adjust}')
        else:
            inflow_level_adjust = 0
        
        if alert_emergency_button == True:
            inflow_level = val
            inflow_level_adjust = 0

        # mute_count
        mute = False
        val = get_data(key='mute_count', file='interface')
        if val > mute_count:
            mute = True
            if VERBOSE:
                print(f'mute = {mute}')
        mute_count = val

        if mute == True:
            speaker.stop()

            alert_supply_flow_low = False
            alert_supply_flow_low_timer.reset()

            alert_supply_flow_high = False
            alert_supply_flow_high_timer.reset()

            alert_waste_flow_low = False
            alert_waste_flow_low_timer.reset()

            alert_waste_flow_high = False
            alert_waste_flow_high_timer.reset()

            alert_flow_discrepancy = False
            alert_flow_discrepancy_timer.reset()

            alert_hematuria = False
            alert_hematuria_timer.reset()

        # reset
        reset = get_data(key='reset', file='interface')
        if reset == True:
            for file in ['system', 'interface', 'patient', 'hematuria']:
                delete_data(file=file)
            if VERBOSE:
                print(f'reset = {reset}')
            break
        
        
        # run sensors and calculate, format, and update system data
        # hematuria_percent, hematuria_level
        hematuria_percent = get_data(key='hematuria_percent', file='hematuria')
        hematuria_level = get_data(key='hematuria_level', file='hematuria')
        
        # supply_volume, waste_volume
        # supply_mass = supply_weight_sensor.read(replicates=SUPPLY_WEIGHT_SENSOR_REPLICATES) # old implementation
        # supply_time = time.time()

        # waste_mass = waste_weight_sensor.read(replicates=WASTE_WEIGHT_SENSOR_REPLICATES) # old implementation
        # waste_time = time.time()

        scan = supply_weight_sensor.read(replicates=1)
        scan = scan / SUPPLY_DENSITY # convert g to mL
        supply_scans.insert(0, scan)

        scan = waste_weight_sensor.read(replicates=1)
        scan = scan / WASTE_DENSITY # convert g to mL
        waste_scans.insert(0, scan)

        if iteration > WEIGHT_REPLICATES:
            supply_scans.pop() # remove old data
            temp = supply_scans.copy()
            temp.sort()
            temp = temp[WEIGHT_OUTLIERS:-WEIGHT_OUTLIERS]
            supply_volume = sum(temp)/len(temp)
        else:
            supply_volume = 0
                
        supply_volume_time = time.time()
        
        if iteration > WEIGHT_REPLICATES:
            waste_scans.pop() # remove old data
            temp = waste_scans.copy()
            temp.sort()
            temp = temp[WEIGHT_OUTLIERS:-WEIGHT_OUTLIERS]
            waste_volume = sum(temp)/len(temp)
        else:
            waste_volume = 0
        
        waste_volume_time = time.time()

        supply_volumes.insert(0, supply_volume)
        supply_volume_times.insert(0, supply_volume_time)
        waste_volumes.insert(0, waste_volume)
        waste_volume_times.insert(0, waste_volume_time)

        supply_volume = min(supply_volume_total, supply_volume)
        supply_volume = max(0, supply_volume)

        waste_volume = min(waste_volume_total, waste_volume)
        waste_volume = max(0, waste_volume)

        # supply_rate, waste_rate
        if iteration > FLOW_RATE_REPLICATES:
            supply_volumes.pop() # remove old data
            supply_volume_times.pop()
            waste_volumes.pop()
            waste_volume_times.pop()

            if iteration > FLOW_RATE_REPLICATES + WEIGHT_REPLICATES:
                regression.fit(np.array(supply_volume_times).reshape(-1, 1), np.array(supply_volumes).reshape(-1, 1))
                supply_rate = regression.coef_[0][0] * -60 # convert mL/s to mL/min
                supply_rate = max(0, supply_rate)

                regression.fit(np.array(waste_volume_times).reshape(-1, 1), np.array(waste_volumes).reshape(-1, 1))
                waste_rate = regression.coef_[0][0] * 60 # convert mL/s to mL/min
                waste_rate = max(0, waste_rate)

            else:
                supply_rate = 0
                waste_rate = 0
            
        else:
            supply_rate = 0
            waste_rate = 0

        # supply_percent
        supply_percent = (supply_volume / supply_volume_total) * 100.0

        # supply_time
        if supply_rate > 1:
            supply_time = supply_volume / supply_rate
            if supply_time > 5999:
                supply_time = 5999 # 99 h 59 m
        else:
            supply_time = 5999 # 99 h 59 m
        
        # waste_percent
        waste_percent = (waste_volume / waste_volume_total) * 100.0
        
        # waste_time
        if waste_rate > 0.001:
            waste_time = (waste_volume_total - waste_volume) / waste_rate
            if waste_time > 5999:
                waste_time = 5999 # 99 h 59 m
        else:
            waste_time = 5999 # 99 h 59 m

        # date, time
        current_date = datetime.now(pytz.utc).strftime("%m/%d/%Y")
        current_time = datetime.now(pytz.utc).strftime("%H:%M:%S")

        # active_time
        datetime_1 = f"{start_date} {start_time}"
        datetime_2 = f"{current_date} {current_time}"

        format = "%m/%d/%Y %H:%M:%S"
        dt1 = datetime.strptime(datetime_1, format)
        dt2 = datetime.strptime(datetime_2, format)
        diff = dt2 - dt1
        
        active_time = diff.total_seconds() / 60

        # adjust inflow rate
        if alert_emergency_button == False:
            if automatic == True:
                if DEMO: # FOR DEMO
                    if hematuria_percent < 0.7:
                        retraction_count = 0
                        linear_actuator.extend(duty_cycle=100, duration=INFLOW_ADJUSTMENT_TIME) # FOR DEMO
                    else:
                        if retraction_count <= 10:
                            retraction_count += 1
                            linear_actuator.retract(duty_cycle=100, duration=INFLOW_ADJUSTMENT_TIME) # FOR DEMO
                else:
                    output = pid(hematuria_percent)
                    if output > 0:
                        linear_actuator.retract(duty_cycle=100, duration=output)
                    elif output < 0:
                        linear_actuator.extend(duty_cycle=100, duration=2*abs(output))

            else:
                if inflow_level_adjust == 1:
                    linear_actuator.retract(duty_cycle=100, duration=INFLOW_ADJUSTMENT_TIME)
                    inflow_level_adjust = 0
                elif inflow_level_adjust == -1:
                    linear_actuator.extend(duty_cycle=100, duration=INFLOW_ADJUSTMENT_TIME)
                    inflow_level_adjust = 0
                else:
                    time.sleep(INFLOW_ADJUSTMENT_TIME)

        elif alert_emergency_button == True:
            linear_actuator.extend(duty_cycle=100, duration=10*INFLOW_ADJUSTMENT_TIME) # extend actuator
        
        # check alert conditions
        status_level = ALERT_NORMAL_STATUS
        status_message = ALERT_NORMAL_MESSAGE
        
        new_alert = False
        
        # CAUTION
        # alert_supply_low
        if supply_percent < ALERT_SUPPLY_LOW_PERCENT:
            if alert_supply_low == False:
                new_alert = True
            alert_supply_low = True
            status_level = ALERT_SUPPLY_LOW_LEVEL
            status_message = ALERT_SUPPLY_LOW_MESSAGE
        else:
            alert_supply_low = False

        # alert_waste_high
        if waste_percent > ALERT_WASTE_HIGH_PERCENT:
            if alert_waste_high == False:
                new_alert = True
            alert_waste_high = True
            status_level = ALERT_WASTE_HIGH_LEVEL
            status_message = ALERT_WASTE_HIGH_MESSAGE
        else:
            alert_waste_high = False

        # alert_waste_flow_high
        if waste_rate > ALERT_WASTE_FLOW_HIGH_RATE:
            alert_waste_flow_high_timer.start()
        else:
            alert_waste_flow_high_timer.reset()
            alert_waste_flow_high = False
        
        duration = alert_waste_flow_high_timer.duration(unit='min')
        if duration and duration > ALERT_WASTE_FLOW_HIGH_TIME:
            if alert_waste_flow_high == False:
                new_alert = True
            alert_waste_flow_high = True
            status_level = ALERT_WASTE_FLOW_HIGH_LEVEL
            status_message = ALERT_WASTE_FLOW_HIGH_MESSAGE

        # alert_supply_flow_high
        if supply_rate > ALERT_SUPPLY_FLOW_HIGH_RATE:
            alert_supply_flow_high_timer.start()
        else:
            alert_supply_flow_high_timer.reset()
            alert_supply_flow_high = False
        
        duration = alert_supply_flow_high_timer.duration(unit='min')
        if duration and duration > ALERT_SUPPLY_FLOW_HIGH_TIME:
            if alert_supply_flow_high == False:
                new_alert = True
            alert_supply_flow_high = True
            status_level = ALERT_SUPPLY_FLOW_HIGH_LEVEL
            status_message = ALERT_SUPPLY_FLOW_HIGH_MESSAGE

        # CRITICAL
        # alert_supply_flow_low
        if supply_rate < ALERT_SUPPLY_FLOW_LOW_RATE:
            alert_supply_flow_low_timer.start()
        else:
            alert_supply_flow_low_timer.reset()
            alert_supply_flow_low = False
        
        duration = alert_supply_flow_low_timer.duration(unit='min')
        if duration and duration > ALERT_SUPPLY_FLOW_LOW_TIME:
            if alert_supply_flow_low == False:
                new_alert = True
            alert_supply_flow_low = True
            status_level = ALERT_SUPPLY_FLOW_LOW_LEVEL
            status_message = ALERT_SUPPLY_FLOW_LOW_MESSAGE

        # alert_waste_flow_low
        if waste_rate < ALERT_WASTE_FLOW_LOW_RATE:
            alert_waste_flow_low_timer.start()
        else:
            alert_waste_flow_low_timer.reset()
            alert_waste_flow_low = False
        
        duration = alert_waste_flow_low_timer.duration(unit='min')
        if duration and duration > ALERT_WASTE_FLOW_LOW_TIME:
            if alert_waste_flow_low == False:
                new_alert = True
            alert_waste_flow_low = True
            status_level = ALERT_WASTE_FLOW_LOW_LEVEL
            status_message = ALERT_WASTE_FLOW_LOW_MESSAGE

        # alert_flow_discrepancy
        if supply_rate - waste_rate > ALERT_FLOW_DISCREPANCY_RATE:
            alert_flow_discrepancy_timer.start()
        else:
            alert_flow_discrepancy_timer.reset()
            alert_flow_discrepancy = False
        
        duration = alert_flow_discrepancy_timer.duration(unit='min')
        if duration and duration > ALERT_FLOW_DISCREPANCY_TIME:
            if alert_flow_discrepancy == False:
                new_alert = True
            alert_flow_discrepancy = True
            status_level = ALERT_FLOW_DISCREPANCY_LEVEL
            status_message = ALERT_FLOW_DISCREPANCY_MESSAGE

        # alert_hematuria
        if hematuria_level > ALERT_HEMATURIA_SEVERITY:
            alert_hematuria_timer.start()
        else:
            alert_hematuria_timer.reset()
            alert_hematuria = False
        
        duration = alert_hematuria_timer.duration(unit='min')
        if duration and duration > ALERT_HEMATURIA_TIME:
            if alert_hematuria == False:
                new_alert = True
            alert_hematuria = True
            status_level = ALERT_HEMATURIA_LEVEL
            status_message = ALERT_HEMATURIA_MESSAGE

        # alert_emergency_button
        if alert_emergency_button == True:
            if alert_emergency == False:
                new_alert = True
            alert_emergency = True
            status_level = ALERT_EMERGENCY_BUTTON_LEVEL
            status_message = ALERT_EMERGENCY_BUTTON_MESSAGE

        if DEMO:
            status_level = ALERT_NORMAL_STATUS
            status_message = ALERT_NORMAL_MESSAGE

            # alert_supply_low FOR DEMO
            if supply_percent < ALERT_SUPPLY_LOW_PERCENT:
                if alert_supply_low == False:
                    new_alert = True
                alert_supply_low = True
                status_level = ALERT_SUPPLY_LOW_LEVEL
                status_message = ALERT_SUPPLY_LOW_MESSAGE
            else:
                alert_supply_low = False

            # alert_waste_high FOR DEMO
            if waste_percent > ALERT_WASTE_HIGH_PERCENT:
                if alert_waste_high == False:
                    new_alert = True
                alert_waste_high = True
                status_level = ALERT_WASTE_HIGH_LEVEL
                status_message = ALERT_WASTE_HIGH_MESSAGE
            else:
                alert_waste_high = False

            # alert_emergency_button FOR DEMO
            if alert_emergency_button == True:
                if alert_emergency == False:
                    new_alert = True
                alert_emergency = True
                status_level = ALERT_EMERGENCY_BUTTON_LEVEL
                status_message = ALERT_EMERGENCY_BUTTON_MESSAGE
        
        # update light color and speaker sound according to status_level and new_alert
        if iteration > FLOW_RATE_REPLICATES + WEIGHT_REPLICATES:
            if status_level == 'NORMAL':
                light.color(color='green')
            elif status_level == 'CAUTION':
                light.color(color='yellow')
            elif status_level == 'CRITICAL':
                light.color(color='red')

            # if status_level == 'NORMAL':
            #     speaker.stop()
            if status_level == 'CAUTION' and new_alert == True:
                speaker.play(file=ALERT_CAUTION_SOUND)
            elif status_level == 'CRITICAL' and new_alert == True:
                speaker.play(file=ALERT_CRITICAL_SOUND)
            
        else:
            light.color(color='yellow')
            status_level = ALERT_STARTUP_STATUS
            status_message = ALERT_STARTUP_MESSAGE


        # add updated system data to database
        data = {
            'hematuria_level': round(hematuria_level),
            'hematuria_percent': float(hematuria_percent),
            'supply_percent': round(supply_percent),
            'supply_volume': round(supply_volume),
            'supply_time': round(supply_time),
            'supply_rate': round(supply_rate, -1),
            'waste_percent': round(waste_percent),
            'waste_volume': round(waste_volume),
            'waste_time': round(waste_time),
            'waste_rate': round(waste_rate, -1),
            'status_level': status_level,
            'status_message': status_message,
            'active_time': round(active_time),
            'current_date': current_date,
            'current_time': current_time,
            'supply_volume_total': round(supply_volume_total),
            'supply_volume_gross': round(supply_volume_gross + (supply_volume_total - supply_volume)),
            'supply_replace_count': int(supply_replace_count),
            'waste_volume_total': round(waste_volume_total),
            'waste_volume_gross': round(waste_volume_gross + waste_volume),
            'waste_replace_count': int(waste_replace_count),
            'automatic': bool(automatic),
            'inflow_level': round(inflow_level),
            'mute': bool(mute)
            }
        
        add_data(data=data, file='system')
        iteration += 1


        # remove outdated system data and interface data
        system_entry = get_data(key='entry', file='system', n=1)
        if system_entry > 10000:
            remove_data(file='system', n=system_entry-10000)
        
        interface_entry = get_data(key='entry', file='interface', n=1)
        if interface_entry > 10000:
            remove_data(file='interface', n=interface_entry-10000)


        # repeat


    # shutdown if reset
    # emergency_button.shutdown()
    # light.shutdown()
    # linear_actuator.shutdown()
    # speaker.shutdown()
    # spectral_sensor.shutdown() # run separately
    # supply_weight_sensor.shutdown()
    # waste_weight_sensor.shutdown()


if __name__ == '__main__':
    while True:
        main() # run main loop
        time.sleep(2)
