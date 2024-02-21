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

from data import *
from simple_pid import PID

from components.light import Light
from components.linear_actuator import LinearActuator
from components.speaker import Speaker
from components.spectral_sensor import SpectralSensor
from components.weight_sensor import WeightSensor


def main():

    reset = False

    # Initialize databases
    if not os.path.isfile('data/system.db'):
        create_data(file='system', verbose=True)
        reset = True
    if not os.path.isfile('data/user.db'):
        create_data(file='user', verbose=True)
        reset = True
    if not os.path.isfile('data/patient.json'):
        create_data(file='patient', verbose=True)
        reset = True

    system_data = get_data(keys='all', file='system', n=1, order='DESC')
    # need to assign to script variables

    







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
