'''
MAIN

Notes
- Automatically controls irrigation with PID feedback
- Monitors all sensors/peripherals and user interface via the interface.db database
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

from data import *

from components.light import Light
from components.linear_actuator import LinearActuator
from components.speaker import Speaker
from components.spectral_sensor import SpectralSensor
from components.weight_sensor import WeightSensor


# system parameters
INFLOW_ADJUSTMENT_SIZE = 0.005
SPECTRAL_SENSOR_REPLICATES = 10
WEIGHT_SENSOR_REPLICATES = 15

SUPPLY_DENSITY = 1.0
WASTE_DENSITY = 1.0


# function to subtract date-time strings in minutes
def datetime_difference(date_1, time_1, date_2, time_2):
    datetime_1 = f"{date_1} {time_1}"
    datetime_2 = f"{date_2} {time_2}"

    format = "%m/%d/%Y %H:%M:%S"
    dt1 = datetime.strptime(datetime_1, format)
    dt2 = datetime.strptime(datetime_2, format)

    diff = dt2 - dt1
    diff_min = diff.total_seconds() / 60

    return diff_min


# main loop
def main():

    # instantiate components and PID
    light = Light(red_pin=board.D8, green_pin=board.D7, blue_pin=board.D1)
    linear_actuator = LinearActuator(en_pin=10, in1_pin=9, in2_pin=11, freq=1000)
    speaker = Speaker()
    spectral_sensor = SpectralSensor(led_pin=4, use_led=True, sensor_type='VIS', max=48000)
    supply_weight_sensor = WeightSensor(pdsck_pin=18, dout_pin=23, offset=1, scale=1)
    waste_weight_sensor = WeightSensor(pdsck_pin=14, dout_pin=15, offset=1, scale=1)
    
    pid = PID(1, 0.1, 0.05, setpoint=1)

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

    status_level = system_data['status_level']
    _ = system_data['status_message'] # not necessary

    _ = system_data['active_time'] # not necessary
    _ = system_data['date'] # not necessary
    _ = system_data['time'] # not necessary

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

    # define additional variables
    low_supply = False
    low_waste = False
    status_level_prev = ''

    # perform reset if reset
    if reset == True:

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
                supply_weight_sensor.zero(replicates=WEIGHT_SENSOR_REPLICATES) # zero weight sensor
                break
            time.sleep(0.01)
        
        while True:
            val = get_data(key='supply_replace_count_added', file='interface')
            if val > supply_replace_count_added:
                supply_replace_count_added = val
                supply_replace_volume = get_data(key='supply_replace_volume', file='interface')
                supply_weight_sensor.calibrate(known_mass=supply_replace_volume, replicates=WEIGHT_SENSOR_REPLICATES) # calibrate weight sensor with known mass
                supply_volume_total = supply_replace_volume # update
                supply_replace_count += 1 # update
                break
            time.sleep(0.01)
        
        # wait for replaced waste bag
        while True:
            val = get_data(key='waste_replace_count_removed', file='interface')
            if val > waste_replace_count_removed:
                waste_replace_count_removed = val
                waste_weight_sensor.zero(replicates=WEIGHT_SENSOR_REPLICATES) # zero weight sensor
                break
            time.sleep(0.01)
        
        while True:
            val = get_data(key='waste_replace_count_added', file='interface')
            if  val > waste_replace_count_added:
                waste_replace_count_added = val
                waste_replace_volume = get_data(key='waste_replace_volume', file='interface')
                waste_weight_sensor.calibrate(known_mass=waste_replace_volume, replicates=WEIGHT_SENSOR_REPLICATES) # calibrate weight sensor with known mass
                waste_volume_total = waste_replace_volume # update
                waste_replace_count += 1 # update
                break
            time.sleep(0.01)

        # wait for replaced tubing (setup)
        linear_actuator.retract(duty_cycle=100, duration=5) # retract actuator
        while True:
            setup = get_data(key='setup', file='interface')
            if setup == True:
                linear_actuator.extend(duty_cycle=100, duration=10) # extend actuator
                break
            time.sleep(0.01)
    
        reset = False
    
    # get stored patient data from database and assign to variables
    patient_data = get_data(key='all', file='interface')
    
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
    while True:
    
        # get and check user interface data from database
        # supply_replace_volume, supply_replace_count_removed, supply_replace_count_added
        val = get_data(key='supply_replace_count_removed')
        if  val > supply_replace_count_removed:
            supply_replace_count_removed = val
            supply_weight_sensor.zero(replicates=WEIGHT_SENSOR_REPLICATES) # zero weight sensor

        val = get_data(key='supply_replace_count_added', file='interface')
        if val > supply_replace_count_added:
            supply_replace_count_added = val
            supply_replace_volume = get_data(key='supply_replace_volume', file='interface')
            supply_weight_sensor.calibrate(known_mass=supply_replace_volume, replicates=WEIGHT_SENSOR_REPLICATES) # calibrate weight sensor with known mass
            supply_volume_gross +=  supply_volume_total - supply_volume # update
            supply_volume_total = supply_replace_volume # update
            supply_replace_count += 1 # update
            low_supply = False

        # waste_replace_volume, waste_replace_count_removed, waste_replace_count_added
        val = get_data(key='waste_replace_count_removed')
        if  val > waste_replace_count_removed:
            waste_replace_count_removed = val
            waste_weight_sensor.zero(replicates=WEIGHT_SENSOR_REPLICATES) # zero weight sensor'

        val = get_data(key='waste_replace_count_added', file='interface')
        if val > waste_replace_count_added:
            waste_replace_count_added = val
            waste_replace_volume = get_data(key='waste_replace_volume', file='interface')
            waste_weight_sensor.calibrate(known_mass=waste_replace_volume, replicates=WEIGHT_SENSOR_REPLICATES) # calibrate weight sensor with known mass
            waste_volume_gross += waste_volume # update
            supply_volume_total = supply_replace_volume # update
            supply_replace_count += 1 # update
            low_waste = False
            
        # automatic, inflow_level
        automatic = get_data(key='automatic', file='interface')
        val = get_data(key='inflow_level', file='interface')
        inflow_level_adjust = val - inflow_level
        inflow_level = val

        # mute_count
        mute = False
        val = get_data(key='mute_count', file='interface')
        if val > mute_count:
            mute = True
            speaker.stop()
        mute_count = val

        # reset
        reset = get_data(key='reset', file='interface')
        if reset == True:
            for file in ['system', 'interface', 'patient']:
                delete_data(file=file)
            break

        # run sensors
        intensities = spectral_sensor.read(replicates=SPECTRAL_SENSOR_REPLICATES)
        supply_mass = supply_weight_sensor.read(replicates=WEIGHT_SENSOR_REPLICATES)
        waste_mass = waste_weight_sensor.read(replicates=WEIGHT_SENSOR_REPLICATES)

        # calculate, format, and update system data
        hematuria_percent = 0 # from regression analysis TODO
        hematuria_level = 0 # from survey TODO
        
        supply_volume = supply_mass / SUPPLY_DENSITY
        supply_volume = min(supply_volume_total, supply_volume)
        supply_volume = max(0, supply_volume)

        supply_percent = (supply_volume / supply_volume_total) * 100.0

        supply_rate = 

        supply_time = supply_volume / supply_rate
        
        waste_volume = waste_mass / WASTE_DENSITY
        waste_volume = min(waste_volume_total, waste_volume)
        waste_volume = max(0, waste_volume)

        waste_percent = (waste_volume / waste_volume_total) * 100.0

        waste_rate = 

        waste_time = waste_volume / waste_rate

        date = datetime.now().strftime("%m/%d/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        active_time = datetime_difference(start_date, start_time, date, time)

        # adjust inflow rate
        if automatic == True:
            inflow_level_adjust = round(pid(hematuria_percent))
        
        if inflow_level_adjust > 0:
            for _ in range(inflow_level_adjust):
                linear_actuator.retract(duty_cycle=100, duration=INFLOW_ADJUSTMENT_SIZE)
        elif inflow_level_adjust < 0:
            for _ in range(abs(inflow_level_adjust)):
                linear_actuator.extend(duty_cycle=100, duration=INFLOW_ADJUSTMENT_SIZE)

        # check alert conditions
        status_level = ''

        status_message = ''
        
        if supply_percent < 10:
            if low_supply == False:
                new_alert = True
            low_supply = True
        
        if waste_percent < 10:
            if low_waste == False:
                new_alert = True
            low_waste = True

        if low_supply == True or low_waste == True:
            status_level = 'CAUTION'
            status_message = ''
        

        
        if status_level == 'CAUTION' and (new_alert == True) and mute == False:
            speaker.play(file='sound/chime.mp3')
        elif status_level == 'CRITICAL' and (status_message != status_message_prev) and mute == False:
            speaker.play(file='sound/alarm.mp3')

        if status_level == 'NORMAL':
            light.color(color='default')
        elif status_level == 'CAUTION':
            light.color(color='orange')
        elif status_level == 'CRITICAL':
            light.color(color='red')

        status_level_prev = status_level

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
            'date': date,
            'time': time,
            'supply_volume_total': round(supply_volume_total),
            'supply_volume_gross': round(supply_volume_gross),
            'supply_replace_count': int(supply_replace_count),
            'waste_volume_total': round(waste_volume_total),
            'waste_volume_gross': round(waste_volume_gross),
            'waste_replace_count': int(waste_replace_count),
            'automatic': bool(automatic),
            'inflow_level': round(inflow_level),
            'mute': bool(mute)
            }
        
        add_data(data=data, file='system')

        # remove old system data from database
        # remove_data(...)

        # repeat

    # shutdown
    light.shutdown()
    linear_actuator.shutdown()
    speaker.shutdown()
    spectral_sensor.shutdown()
    supply_weight_sensor.shutdown()
    waste_weight_sensor.shutdown()





# FROM WEIGTH SENSOR
# def rate(self, interval=60):
#     start_time = time.time()
#     duration = 0

#     start_mass = 0
#     end_mass = 0
#     masses = []
#     calculate_start_mass = True

#     while duration <= interval:
#         duration = time.time() - start_time
#         mass = self.mass()

#         if duration <= 1:
#             masses.append(mass)
            
#         elif duration > 1 and calculate_start_mass:
#             start_mass = np.mean(masses)
#             masses = []
#             calculate_start_mass = False

#         elif duration >= interval - 1:
#             masses.append(mass)

#         elif duration >= interval:
#             end_mass = np.mean(masses)
#             rate = ((start_mass - end_mass)/duration)*60
#             if self.verbose:
#                 print(f"WeightSensor: rate = {rate} mg/min")
#             return rate





# FROM SPECTRAL SENSOR
# def level(self, weights, bias, max_level, replicates=10, range=[0, 100]):
#     reading = self.read(replicates)
#     intensities = list(reading.values())

#     level = sum([w*i for w, i in zip(weights, intensities[0:4])]) + bias # apply least squares regression weights and bias to predict level
#     level = max(level, range[0])
#     level = min(level, range[1])

#     rescaled_level = int((level/max_level * (range[1]-range[0])) + range[0])
    
#     if self.verbose:
#         print(f"SpectralSensor: level = {rescaled_level} in range [{range[0]}-{range[1]}]")

#     return rescaled_level # return rescaled level


if __name__ == '__main__':
    while True:
        main() # run main loop
        time.sleep(1)
