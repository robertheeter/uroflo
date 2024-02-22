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

    # instantiate components
    light = Light(red_pin=board.D8, green_pin=board.D7, blue_pin=board.D1)
    linear_actuator = LinearActuator(en_pin=10, in1_pin=9, in2_pin=11, freq=1000)
    speaker = Speaker()
    spectral_sensor = SpectralSensor(led_pin=4, use_led=True, sensor_type='VIS', max=48000)
    supply_weight_sensor = WeightSensor(pdsck_pin=18, dout_pin=23, offset=1, scale=1)
    waste_weight_sensor = WeightSensor(pdsck_pin=14, dout_pin=15, offset=1, scale=1)
    
    # check reset condition
    reset = False
    for file in ['system', 'user', 'patient']:
        if not exists_data(file=file):
            reset = True

    # initialize new databases if reset
    if reset == True:
        for file in ['system', 'user', 'patient']:
            delete_data(file=file)
            create_data(file=file)
    
    # get current system data and assign to variables
    system_data = get_data(key='all', file='system')

    hematuria_level = system_data['hematuria_level']
    hematuria_percent = system_data['hematuria_percent']

    supply_percent = system_data['supply_percent']
    supply_volume = system_data['supply_volume']
    supply_time = system_data['supply_time']
    supply_rate = system_data['supply_rate']

    waste_percent = system_data['waste_percent']
    waste_volume = system_data['waste_volume']
    waste_time = system_data['waste_time']
    waste_rate = system_data['waste_rate']

    status_level = system_data['status_level']
    status_message = system_data['status_message']

    active_time = system_data['active_time']
    date = system_data['date']
    time = system_data['time']

    supply_volume_total = system_data['supply_volume_total']
    supply_volume_gross = system_data['supply_volume_gross']
    supply_replace_count = system_data['supply_replace_count']

    waste_volume_total = system_data['waste_volume_total']
    waste_volume_gross = system_data['waste_volume_gross']
    waste_replace_count = system_data['waste_replace_count']

    automatic = system_data['automatic']
    inflow_level = system_data['inflow_level']

    mute = system_data['mute']

    # get current user data and assign to variables
    user_data = get_data(key='all', file='user')

    supply_replace_volume = user_data['supply_replace_volume']
    supply_replace_count_removed = user_data['supply_replace_count_removed']
    supply_replace_count_added = user_data['supply_replace_count_added']

    waste_replace_volume = user_data['waste_replace_volume']
    waste_replace_count_removed = user_data['waste_replace_count_removed']
    waste_replace_count_added = user_data['waste_replace_count_added']

    automatic = user_data['automatic']
    automatic = user_data['automatic']

    automatic = user_data['automatic']

    automatic = user_data['automatic']
    automatic = user_data['automatic']

    # perform reset procedure
    if reset == True:
        linear_actuator.retract(duty_cycle=100, duration=10) # retract actuator
        
        # wait for patient info update
        while True:
            lastname = get_data(key='lastname', file='patient')
            if lastname != '':
                break
            time.sleep(0.01)

        # wait for replaced supply bag
        while True:
            if get_data(key='supply_replace_count_removed', file='user') > supply_replace_count_removed:
                supply_weight_sensor.zero(replicates=15) # zero weight sensor
                break
            time.sleep(0.01)
        
        while True:
            supply_replace_count_added = get_data(key='supply_replace_count_added', file='user')
            if supply_replace_count_added == 1:
                supply_replace_volume = get_data(key='supply_replace_volume', file='user')
                supply_weight_sensor.calibrate(known_mass=supply_replace_volume, replicates=15) # calibrate weight sensor with known mass
                supply_volume_total = supply_replace_volume # update
                supply_replace_count = 1 # update
                break
            time.sleep(0.01)
        
        # wait for replaced waste bag
        while True:
            waste_replace_count_removed = get_data(key='waste_replace_count_removed', file='user')
            if waste_replace_count_removed == 1:
                waste_weight_sensor.zero(replicates=15) # zero weight sensor
                break
            time.sleep(0.01)
        
        while True:
            waste_replace_count_added = get_data(key='waste_replace_count_added', file='user')
            if waste_replace_count_added == 1:
                waste_replace_volume = get_data(key='waste_replace_volume', file='user')
                waste_weight_sensor.calibrate(known_mass=waste_replace_volume, replicates=15) # calibrate weight sensor with known mass
                waste_volume_total = waste_replace_volume # update
                waste_replace_count = 1 # update
                break
            time.sleep(0.01)

        # wait for replaced tubing
        while True:
            setup = get_data(key='setup', file='user')
            if setup == True:
                linear_actuator.extend(duty_cycle=100, duration=10) # extend actuator
                break
            time.sleep(0.01)
    

    # begin normal operation
    while True:

        user_data = get_data(key='all', file='user')
        
        supply_replace_removed = get_data(key='supply_replace_removed')

        # example implementations
        for color in ['default', 'off', 'yellow', 'orange', 'red']:
            light.color(color=color)
            time.sleep(4)

        linear_actuator.retract(duty_cycle=100, duration=4)
        linear_actuator.extend(duty_cycle=100, duration=8)

        for file in ['sound/chime.mp3', 'sound/alarm.mp3']:
            speaker.play(file=file, volume=1.0)
            time.sleep(10)

        reading = spectral_sensor.read(replicates=10)

        reading = supply_weight_sensor.read(replicates=15)

        reading = waste_weight_sensor.read(replicates=15)



        # reset condition
        if True:
            break

    
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
        time.sleep(10)
