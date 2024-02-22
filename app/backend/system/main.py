'''
MAIN

Notes
- Automatically controls irrigation with PID feedback
- Monitors all sensors/peripherals and user interface via the user.db database
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
    for file in ['system', 'user', 'patient']:
        if not exists_data(file=file):
            reset = True

    # initialize new data if reset
    if reset == True:
        for file in ['system', 'user', 'patient']:
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

    _ = system_data['status_level'] # not necessary
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

    # get stored user data from database and assign to variables
    user_data = get_data(key='all', file='user')

    supply_replace_volume = user_data['supply_replace_volume']
    supply_replace_count_removed = user_data['supply_replace_count_removed']
    supply_replace_count_added = user_data['supply_replace_count_added']
    
    waste_replace_volume = user_data['waste_replace_volume']
    waste_replace_count_removed = user_data['waste_replace_count_removed']
    waste_replace_count_added = user_data['waste_replace_count_added']

    automatic = user_data['automatic']
    inflow_level = user_data['inflow_level']

    mute_count = user_data['mute_count']

    _ = user_data['setup'] # not necessary
    _ = user_data['reset'] # not necessary

    # get stored patient data from database and assign to variables
    patient_data = get_data(key='all', file='user')
    
    _ = patient_data['firstname'] # not necessary (add back for alert SMS texting)
    _ = patient_data['lastname'] # not necessary (add back for alert SMS texting)
    _ = patient_data['MRN'] # not necessary (add back for alert SMS texting)
    _ = patient_data['DOB'] # not necessary (add back for alert SMS texting)
    _ = patient_data['sex'] # not necessary (add back for alert SMS texting)
    _ = patient_data['contact_A'] # not necessary (add back for alert SMS texting)
    _ = patient_data['contact_B'] # not necessary (add back for alert SMS texting)

    start_date = patient_data['start_date']
    start_time = patient_data['start_time']
    
    # ensure consistency between databases
    supply_volume_total = supply_replace_volume
    waste_volume_total = waste_replace_volume

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
            val = get_data(key='supply_replace_count_removed', file='user')
            if  val > supply_replace_count_removed:
                supply_replace_count_removed = val
                supply_weight_sensor.zero(replicates=15) # zero weight sensor
                break
            time.sleep(0.01)
        
        while True:
            val = get_data(key='supply_replace_count_added', file='user')
            if val > supply_replace_count_added:
                supply_replace_count_added = val
                supply_replace_volume = get_data(key='supply_replace_volume', file='user')
                supply_weight_sensor.calibrate(known_mass=supply_replace_volume, replicates=15) # calibrate weight sensor with known mass
                supply_volume_total = supply_replace_volume # update
                supply_replace_count += 1 # update
                break
            time.sleep(0.01)
        
        # wait for replaced waste bag
        while True:
            val = get_data(key='waste_replace_count_removed', file='user')
            if val > waste_replace_count_removed:
                waste_replace_count_removed = val
                waste_weight_sensor.zero(replicates=15) # zero weight sensor
                break
            time.sleep(0.01)
        
        while True:
            val = get_data(key='waste_replace_count_added', file='user')
            if  val > waste_replace_count_added:
                waste_replace_count_added = val
                waste_replace_volume = get_data(key='waste_replace_volume', file='user')
                waste_weight_sensor.calibrate(known_mass=waste_replace_volume, replicates=15) # calibrate weight sensor with known mass
                waste_volume_total = waste_replace_volume # update
                waste_replace_count += 1 # update
                break
            time.sleep(0.01)

        # wait for replaced tubing (setup)
        linear_actuator.retract(duty_cycle=100, duration=5) # retract actuator
        while True:
            setup = get_data(key='setup', file='user')
            if setup == True:
                linear_actuator.extend(duty_cycle=100, duration=10) # extend actuator
                break
            time.sleep(0.01)
    
        reset = False
    
    # begin normal operation
    while True:
    
        # get and check user data from database
        # supply_replace_volume, supply_replace_count_removed, supply_replace_count_added
        val = get_data(key='supply_replace_count_removed')
        if  val > supply_replace_count_removed:
            supply_replace_count_removed = val
            supply_weight_sensor.zero(replicates=15) # zero weight sensor

        val = get_data(key='supply_replace_count_added', file='user')
        if val > supply_replace_count_added:
            supply_replace_count_added = val
            supply_replace_volume = get_data(key='supply_replace_volume', file='user')
            supply_weight_sensor.calibrate(known_mass=supply_replace_volume, replicates=15) # calibrate weight sensor with known mass
            supply_volume_gross +=  supply_volume_total - supply_volume # update
            supply_volume_total = supply_replace_volume # update
            supply_replace_count += 1 # update

        # waste_replace_volume, waste_replace_count_removed, waste_replace_count_added
        val = get_data(key='waste_replace_count_removed')
        if  val > waste_replace_count_removed:
            waste_replace_count_removed = val
            waste_weight_sensor.zero(replicates=15) # zero weight sensor

        val = get_data(key='waste_replace_count_added', file='user')
        if val > waste_replace_count_added:
            waste_replace_count_added = val
            waste_replace_volume = get_data(key='waste_replace_volume', file='user')
            waste_weight_sensor.calibrate(known_mass=waste_replace_volume, replicates=15) # calibrate weight sensor with known mass
            waste_volume_gross += waste_volume # update
            supply_volume_total = supply_replace_volume # update
            supply_replace_count += 1 # update
            
        # automatic, inflow_level
        automatic = get_data(key='automatic', file='user')
        val = get_data(key='inflow_level', file='user')
        if val > inflow_level:
            inflow_level_increase = val - inflow_level
        elif val < inflow_level:
            inflow_level_decrease = inflow_level - val
        inflow_level = val

        # mute_count
        val = get_data(key='mute_count', file='user')
        if val > mute_count:
            mute = True
        mute_count = val

        # reset
        reset = get_data(key='reset', file='user')
        if reset == True:
            for file in ['system', 'user', 'patient']:
                delete_data(file=file)
            break



        





        # CONTINUE HERE










        # run sensors
        # hematuria sensor

        # supply weight sensor

        # waste weight sensor

            # example implementation
        reading = spectral_sensor.read(replicates=10)
        reading = supply_weight_sensor.read(replicates=15)
        reading = waste_weight_sensor.read(replicates=15)



        # calculate, format, and update system data
        hematuria_percent = 
        hematuria_level = 
        
        supply_volume = 
        supply_percent = 
        supply_rate = 
        supply_time = 
        
        waste_volume = 
        waste_percent = 
        waste_rate = 
        waste_time = 

        active_time = # using start_date and start_time
        date = datetime.now().strftime("%m/%d/%Y")
        time = datetime.now().strftime("%H:%M:%S")

        # adjust inflow rate
        if automatic == True:
            # PID control
            # output = pid(hematuria_level or hematuria_percent)
            # example implementation
            linear_actuator.retract(duty_cycle=100, duration=4)
            linear_actuator.extend(duty_cycle=100, duration=8)
            pass
        else:
            # manual flow rate control with inflow_level_increase and inflow_level_decrease
            # example implementation
            linear_actuator.retract(duty_cycle=100, duration=4)
            linear_actuator.extend(duty_cycle=100, duration=8)

            pass

        # check alert conditions
        status_level =
        status_message = 

            # example implementations
        for color in ['default', 'off', 'yellow', 'orange', 'red']:
            light.color(color=color)
            time.sleep(4)

        for file in ['sound/chime.mp3', 'sound/alarm.mp3']:
            speaker.play(file=file, volume=1.0)
            time.sleep(10)



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
        main()
        time.sleep(1)
