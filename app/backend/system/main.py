'''
MAIN

Notes
- Automatically controls irrigation with PID feedback
- Checks all sensors/peripherals via the hematuria.json and mass.json databases
- Monitors and reacts to the user interface via the interface.db database
- Initiates alerts
- Updates system.db database

Documentation
- PID feedback guide: https://simple-pid.readthedocs.io/en/latest/index.html

'''

import os
import time
import numpy as np
from datetime import datetime
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


# system parameters
INFLOW_ADJUSTMENT_TIME = 0.005 # sec

SUPPLY_WEIGHT_SENSOR_REPLICATES = 15
WASTE_WEIGHT_SENSOR_REPLICATES = 15
FLOW_RATE_REPLICATES = 5 # number of weight measurements to use for each rate calculation

SUPPLY_DENSITY = 1.0 # g/mL
WASTE_DENSITY = 1.0 # g/mL

# alert parameters
ALERT_SUPPLY_LOW_PERCENT = 10
ALERT_SUPPLY_LOW_LEVEL = 'ALERT' # if changing, adjust order of alert conditions below
ALERT_SUPPLY_LOW_MESSAGE = f'Supply bag volume <{ALERT_SUPPLY_LOW_PERCENT}%.'

ALERT_SUPPLY_EMPTY_PERCENT = 5
ALERT_SUPPLY_EMPTY_LEVEL = 'CAUTION' # if changing, adjust order of alert conditions below
ALERT_SUPPLY_EMPTY_MESSAGE = f'Supply bag volume <{ALERT_SUPPLY_EMPTY_PERCENT}%.'

ALERT_WASTE_HIGH_PERCENT = 90
ALERT_WASTE_HIGH_LEVEL = 'ALERT' # if changing, adjust order of alert conditions below
ALERT_WASTE_HIGH_MESSAGE = f'Waste bag volume >{ALERT_WASTE_HIGH_PERCENT}%.'

ALERT_WASTE_FULL_PERCENT = 95
ALERT_WASTE_FULL_LEVEL = 'CAUTION' # if changing, adjust order of alert conditions below
ALERT_WASTE_FULL_MESSAGE = f'Waste bag volume >{ALERT_WASTE_FULL_PERCENT}%.'

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
ALERT_WASTE_FLOW_HIGH_LEVEL = 'ALERT' # if changing, adjust order of alert conditions below
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
    light = Light(red_pin=board.D8, green_pin=board.D7, blue_pin=board.D1)
    linear_actuator = LinearActuator(en_pin=13, in1_pin=19, in2_pin=26, freq=1000)
    speaker = Speaker()
    # spectral_sensor = SpectralSensor(led_pin=4, use_led=True, sensor_type='VIS', max=48000) # not directly used for measurements
    supply_weight_sensor = WeightSensor(pdsck_pin=18, dout_pin=23, offset=1, scale=1)
    waste_weight_sensor = WeightSensor(pdsck_pin=14, dout_pin=15, offset=1, scale=1)
    emergency_button = Button(pin=10)

    pid = PID(1, 0.1, 0.05, setpoint=1)
    regression = LinearRegression()

    # check if reset
    reset = False
    for file in ['system', 'interface', 'patient']:
        if not exists_data(file=file):
            reset = True
            break
    
    # initialize new data if reset
    if reset == True:
        for file in ['system', 'interface', 'patient']:
            delete_data(file=file)
            create_data(file=file)
    
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

    _ = system_data['status_level']
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

    # lists for calculating flow rates
    supply_volumes = []
    supply_times = []
    waste_volumes = []
    waste_times = []

    # additional variables for checking alert conditions
    supply_flow_started = False # prevent alert when device is starting up
    waste_flow_started = False # prevent alert when device is starting up

    alert_supply_low = False
    alert_supply_empty = False

    alert_waste_high = False
    alert_waste_full = False

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

    # perform reset if reset
    if reset == True:
        print('reset')

        # wait for patient info update (NOT NECESSARY?)
        while True:
            lastname = get_data(key='lastname', file='patient')
            sex = get_data(key='sex', file='patient')
            if lastname != '' and sex in ['M', 'F']:
                break
            time.sleep(0.01)

        # wait for replaced supply bag
        while True:
            val = get_data(key='supply_replace_count_removed', file='interface')
            if  val > supply_replace_count_removed:
                supply_replace_count_removed = val
                supply_weight_sensor.zero(replicates=SUPPLY_WEIGHT_SENSOR_REPLICATES) # zero weight sensor
                break
            time.sleep(0.01)
        
        while True:
            val = get_data(key='supply_replace_count_added', file='interface')
            if val > supply_replace_count_added:
                supply_replace_count_added = val
                supply_replace_volume = get_data(key='supply_replace_volume', file='interface')
                supply_weight_sensor.calibrate(known_mass=supply_replace_volume, replicates=SUPPLY_WEIGHT_SENSOR_REPLICATES) # calibrate weight sensor with known mass
                supply_volume_total = supply_replace_volume # update
                supply_replace_count += 1 # update
                break
            time.sleep(0.01)
        
        # wait for replaced waste bag
        while True:
            val = get_data(key='waste_replace_count_removed', file='interface')
            if val > waste_replace_count_removed:
                waste_replace_count_removed = val
                waste_weight_sensor.zero(replicates=WASTE_WEIGHT_SENSOR_REPLICATES) # zero weight sensor
                break
            time.sleep(0.01)
        
        while True:
            val = get_data(key='waste_replace_count_added', file='interface')
            if  val > waste_replace_count_added:
                waste_replace_count_added = val
                waste_replace_volume = get_data(key='waste_replace_volume', file='interface')
                waste_weight_sensor.calibrate(known_mass=waste_replace_volume, replicates=WASTE_WEIGHT_SENSOR_REPLICATES) # calibrate weight sensor with known mass
                waste_volume_total = waste_replace_volume # update
                waste_replace_count += 1 # update
                break
            time.sleep(0.01)

        # wait for replaced tubing (setup)
        linear_actuator.retract(duty_cycle=100, duration=5) # retract actuator
        while True:
            setup = get_data(key='setup', file='interface')
            if setup == True:
                linear_actuator.extend(duty_cycle=100, duration=10) # fully extend actuator
                break
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
    i = 0 # index for calculating flow rates
    system_entries = 1 # number of entries added to system database
    while True:
        print(f'loop # {system_entries}')

        # check emergency button
        if emergency_button.pressed() == True: # button pressed
            while True:
                if emergency_button.pressed() == False: # button released
                    alert_emergency_button = not alert_emergency_button
                    break
                time.sleep(0.01)
    

        # get and check user interface data from database
        # supply_replace_volume, supply_replace_count_removed, supply_replace_count_added
        val = get_data(key='supply_replace_count_removed', file='interface')
        if  val > supply_replace_count_removed:
            supply_replace_count_removed = val
            supply_weight_sensor.zero(replicates=SUPPLY_WEIGHT_SENSOR_REPLICATES) # zero weight sensor

        val = get_data(key='supply_replace_count_added', file='interface')
        if val > supply_replace_count_added:
            supply_replace_count_added = val
            supply_replace_volume = get_data(key='supply_replace_volume', file='interface')
            supply_weight_sensor.calibrate(known_mass=supply_replace_volume, replicates=SUPPLY_WEIGHT_SENSOR_REPLICATES) # calibrate weight sensor with known mass
            supply_volume_gross +=  supply_volume_total - supply_volume # update
            supply_volume_total = supply_replace_volume # update
            supply_replace_count += 1 # update
            alert_supply_low = False
            alert_supply_empty = False

        # waste_replace_volume, waste_replace_count_removed, waste_replace_count_added
        val = get_data(key='waste_replace_count_removed', file='interface')
        if  val > waste_replace_count_removed:
            waste_replace_count_removed = val
            waste_weight_sensor.zero(replicates=WASTE_WEIGHT_SENSOR_REPLICATES) # zero weight sensor'

        val = get_data(key='waste_replace_count_added', file='interface')
        if val > waste_replace_count_added:
            waste_replace_count_added = val
            waste_replace_volume = get_data(key='waste_replace_volume', file='interface')
            waste_weight_sensor.calibrate(known_mass=waste_replace_volume, replicates=WASTE_WEIGHT_SENSOR_REPLICATES) # calibrate weight sensor with known mass
            waste_volume_gross += waste_volume # update
            supply_volume_total = supply_replace_volume # update
            supply_replace_count += 1 # update
            alert_waste_high = False
            alert_waste_full = False
            
        # automatic, inflow_level
        automatic = get_data(key='automatic', file='interface')
        val = get_data(key='inflow_level', file='interface')
        if val > inflow_level:
            inflow_level_adjust = 1
            inflow_level += 1
        elif val < inflow_level:
            inflow_level_adjust = -1
            inflow_level -= 1

        # mute_count
        mute = False
        val = get_data(key='mute_count', file='interface')
        if val > mute_count:
            mute = True
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
            for file in ['system', 'interface', 'patient']:
                delete_data(file=file)
            break
        
        
        # run weight sensors
        supply_mass = supply_weight_sensor.read(replicates=SUPPLY_WEIGHT_SENSOR_REPLICATES)
        supply_time = time.time()

        waste_mass = waste_weight_sensor.read(replicates=WASTE_WEIGHT_SENSOR_REPLICATES)
        waste_time = time.time()


        # calculate, format, and update system data
        # hematuria_percent, hematuria_level
        hematuria_percent = get_data(key='hematuria_percent', file='hematuria')
        hematuria_level = get_data(key='hematuria_level', file='hematuria')

        # supply_volume, waste_volume
        supply_volume = supply_mass / SUPPLY_DENSITY # convert g to mL
        waste_volume = waste_mass / WASTE_DENSITY # convert g to mL

        supply_volumes.insert(0, supply_volume)
        supply_times.insert(0, supply_time)
        waste_volumes.insert(0, waste_volume)
        waste_times.insert(0, waste_time)

        supply_volume = min(supply_volume_total, supply_volume)
        supply_volume = max(0, supply_volume)

        waste_volume = min(waste_volume_total, waste_volume)
        waste_volume = max(0, waste_volume)

        # supply_rate, waste_rate
        if i >= FLOW_RATE_REPLICATES:
            supply_volumes.pop() # remove old data
            supply_times.pop()
            waste_volumes.pop()
            waste_times.pop()

            regression.fit(np.array(supply_times).reshape(-1, 1), np.array(supply_volumes).reshape(-1, 1))
            supply_rate = regression.coef_[0][0] * 60 # convert mL/s to mL/min

            regression.fit(np.array(waste_times).reshape(-1, 1), np.array(waste_volumes).reshape(-1, 1))
            waste_rate = regression.coef_[0][0] * 60 # convert mL/s to mL/min

            if supply_rate > 5: # mL/min
                supply_flow_started = True
            if waste_rate > 5: # mL/min
                waste_flow_started = True
        else:
            supply_rate = 0
            waste_rate = 0
            i += 1

        # supply_percent, supply_time
        supply_percent = (supply_volume / supply_volume_total) * 100.0

        if supply_rate > 1:
            supply_time = supply_volume / supply_rate
            if supply_time > 5999:
                supply_time = 5999 # 99 h 59 m
        else:
            supply_time = 5999 # 99 h 59 m
        
        # waste_percent, waste_time
        waste_percent = (waste_volume / waste_volume_total) * 100.0
        
        if waste_rate > 0.001:
            waste_time = waste_volume / waste_rate
            if waste_time > 5999:
                waste_time = 5999 # 99 h 59 m
        else:
            waste_time = 5999 # 99 h 59 m

        # date, time
        current_date = datetime.now().strftime("%m/%d/%Y")
        current_time = datetime.now().strftime("%H:%M:%S")

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
                output = round(pid(hematuria_percent)) # UPDATE THIS
                # finish this (needs to move actuator)
            
            elif automatic == False:
                if inflow_level_adjust > 0:
                    linear_actuator.retract(duty_cycle=100, duration=INFLOW_ADJUSTMENT_TIME)
                elif inflow_level_adjust < 0:
                    linear_actuator.extend(duty_cycle=100, duration=INFLOW_ADJUSTMENT_TIME)
                else:
                    time.sleep(INFLOW_ADJUSTMENT_TIME)

        elif alert_emergency_button == True:
            linear_actuator.extend(duty_cycle=100, duration=INFLOW_ADJUSTMENT_TIME) # extend actuator

        # check alert conditions
        status_level = 'NORMAL'
        status_message = 'System and patient normal.'
        
        new_alert = False
        
        # ALERT
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
        
        duration = alert_waste_flow_high_timer.duration(units='min')
        if duration and duration > ALERT_WASTE_FLOW_HIGH_TIME:
            if alert_waste_flow_high == False:
                new_alert = True
            alert_waste_flow_high = True
            status_level = ALERT_WASTE_FLOW_HIGH_LEVEL
            status_message = ALERT_WASTE_FLOW_HIGH_MESSAGE

        # CAUTION
        # alert_supply_empty
        if supply_percent < ALERT_SUPPLY_EMPTY_PERCENT:
            if alert_supply_empty == False:
                new_alert = True
            alert_supply_empty = True
            status_level = ALERT_SUPPLY_EMPTY_LEVEL
            status_message = ALERT_SUPPLY_EMPTY_MESSAGE
        else:
            alert_supply_empty = False
        
        # alert_waste_full
        if waste_percent > ALERT_WASTE_FULL_PERCENT:
            if alert_waste_full == False:
                new_alert = True
            alert_waste_full = True
            status_level = ALERT_WASTE_FULL_LEVEL
            status_message = ALERT_WASTE_FULL_MESSAGE
        else:
            alert_waste_full = False

        # alert_supply_flow_high
        if supply_rate > ALERT_SUPPLY_FLOW_HIGH_RATE:
            alert_supply_flow_high_timer.start()
        else:
            alert_supply_flow_high_timer.reset()
            alert_supply_flow_high = False
        
        duration = alert_supply_flow_high_timer.duration(units='min')
        if duration and duration > ALERT_SUPPLY_FLOW_HIGH_TIME:
            if alert_supply_flow_high == False:
                new_alert = True
            alert_supply_flow_high = True
            status_level = ALERT_SUPPLY_FLOW_HIGH_LEVEL
            status_message = ALERT_SUPPLY_FLOW_HIGH_MESSAGE

        # CRITICAL
        # alert_supply_flow_low
        if supply_flow_started == True and supply_rate < ALERT_SUPPLY_FLOW_LOW_RATE:
            alert_supply_flow_low_timer.start()
        else:
            alert_supply_flow_low_timer.reset()
            alert_supply_flow_low = False
        
        duration = alert_supply_flow_low_timer.duration(units='min')
        if duration and duration > ALERT_SUPPLY_FLOW_LOW_TIME:
            if alert_supply_flow_low == False:
                new_alert = True
            alert_supply_flow_low = True
            status_level = ALERT_SUPPLY_FLOW_LOW_LEVEL
            status_message = ALERT_SUPPLY_FLOW_LOW_MESSAGE

        # alert_waste_flow_low
        if waste_flow_started == True and waste_rate < ALERT_WASTE_FLOW_LOW_RATE:
            alert_waste_flow_low_timer.start()
        else:
            alert_waste_flow_low_timer.reset()
            alert_waste_flow_low = False
        
        duration = alert_waste_flow_low_timer.duration(units='min')
        if duration and duration > ALERT_WASTE_FLOW_LOW_TIME:
            if alert_waste_flow_low == False:
                new_alert = True
            alert_waste_flow_low = True
            status_level = ALERT_WASTE_FLOW_LOW_LEVEL
            status_message = ALERT_WASTE_FLOW_LOW_MESSAGE

        # alert_flow_discrepancy
        if supply_flow_started == True and waste_flow_started == True and supply_rate - waste_rate > ALERT_FLOW_DISCREPANCY_RATE:
            alert_flow_discrepancy_timer.start()
        else:
            alert_flow_discrepancy_timer.reset()
            alert_flow_discrepancy = False
        
        duration = alert_flow_discrepancy_timer.duration(units='min')
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
        
        duration = alert_hematuria_timer.duration(units='min')
        if duration and duration > ALERT_HEMATURIA_TIME:
            if alert_hematuria == False:
                new_alert = True
            alert_hematuria = True
            status_level = ALERT_HEMATURIA_LEVEL
            status_message = ALERT_HEMATURIA_MESSAGE

        # alert_emergency_button
        if alert_emergency_button == True:
            status_level = ALERT_EMERGENCY_BUTTON_LEVEL
            status_message = ALERT_EMERGENCY_BUTTON_MESSAGE

        # update light color and speaker sound according to status_level and new_alert
        if status_level == 'NORMAL':
            light.color(color='default')
        elif status_level == 'ALERT':
            light.color(color='yellow')
        elif status_level == 'CAUTION':
            light.color(color='orange')
        elif status_level == 'CRITICAL':
            light.color(color='red')
        
        if status_level == 'ALERT' and new_alert == True:
            speaker.play(file='sound/chime.mp3')
        elif status_level == 'CAUTION' and new_alert == True:
            speaker.play(file='sound/chime.mp3')
        elif status_level == 'CRITICAL' and new_alert == True:
            speaker.play(file='sound/alarm.mp3')


        # add updated system data to database
        data = {
            'hematuria_level': round(hematuria_level),
            'hematuria_percent': float(hematuria_percent),
            'supply_percent': round(supply_percent),
            'supply_volume': round(supply_volume),
            'supply_time': round(supply_time),
            'supply_rate': round(supply_rate),
            'waste_percent': round(waste_percent),
            'waste_volume': round(waste_volume),
            'waste_time': round(waste_time),
            'waste_rate': round(waste_rate),
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
        

        # remove outdated system data and interface data
        add_data(data=data, file='system')
        system_entries += 1
        
        if system_entries > 5000:
            remove_data(file='system', n=1)
        
        interface_entries = get_data(key='entry', file='interface', n=1)
        if interface_entries >= 5000:
            remove_data(file='interface', n=interface_entries-5000)


        # repeat


    # shutdown if reset
    emergency_button.shutdown()
    light.shutdown()
    linear_actuator.shutdown()
    speaker.shutdown()
    # spectral_sensor.shutdown() # run separately
    supply_weight_sensor.shutdown()
    waste_weight_sensor.shutdown()


if __name__ == '__main__':
    while True:
        main() # run main loop
        time.sleep(2)
