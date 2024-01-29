'''
MAIN SYSTEM

About
- Controls device

Notes
- 

Documentation
- 

'''

import time
import RPi.GPIO as GPIO
import numpy as np


class Main():
    def __init__(self):
        pass






    # FROM WEIGTH SENSOR
    def rate(self, interval=60):
        start_time = time.time()
        duration = 0

        start_mass = 0
        end_mass = 0
        masses = []
        calculate_start_mass = True

        while duration <= interval:
            duration = time.time() - start_time
            mass = self.mass()

            if duration <= 1:
                masses.append(mass)
                
            elif duration > 1 and calculate_start_mass:
                start_mass = np.mean(masses)
                masses = []
                calculate_start_mass = False

            elif duration >= interval - 1:
                masses.append(mass)

            elif duration >= interval:
                end_mass = np.mean(masses)
                rate = ((start_mass - end_mass)/duration)*60
                if self.verbose:
                    print(f"WeightSensor: rate = {rate} mg/min")
                return rate





    # FROM SPECTRAL SENSOR
    def level(self, weights, bias, max_level, replicates=10, range=[0, 100]):
        reading = self.read(replicates)
        intensities = list(reading.values())

        level = sum([w*i for w, i in zip(weights, intensities[0:4])]) + bias # apply least squares regression weights and bias to predict level
        level = max(level, range[0])
        level = min(level, range[1])

        rescaled_level = int((level/max_level * (range[1]-range[0])) + range[0])
        
        if self.verbose:
            print(f"SpectralSensor: level = {rescaled_level} in range [{range[0]}-{range[1]}]")

        return rescaled_level # return rescaled level