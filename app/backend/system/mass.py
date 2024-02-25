'''
MASS

Notes
- Measures supply and waste bag masses and rate of mass change using weight sensors

Documentation
- See components/weight_sensor.py

'''

import os
import time
import numpy as np
from datetime import datetime

from data import *

from components.spectral_sensor import SpectralSensor
from components.weight_sensor import WeightSensor


# sensor parameters
SPECTRAL_SENSOR_REPLICATES = 20
SUPPLY_WEIGHT_SENSOR_REPLICATES = 15
WASTE_WEIGHT_SENSOR_REPLICATES = 15

def sensor():

    # instantiate components and PID
    spectral_sensor = SpectralSensor(led_pin=4, use_led=True, sensor_type='VIS', max=48000)
    supply_weight_sensor = WeightSensor(pdsck_pin=18, dout_pin=23, offset=1, scale=1)
    waste_weight_sensor = WeightSensor(pdsck_pin=14, dout_pin=15, offset=1, scale=1)

    # run continuously
    while True:
        hematuria_intensities = spectral_sensor.read(replicates=SPECTRAL_SENSOR_REPLICATES)

        hematuria_purple = hematuria_intensities[450]
        hematuria_blue = hematuria_intensities[500]
        hematuria_green = hematuria_intensities[550]
        hematuria_yellow = hematuria_intensities[570]
        hematuria_orange = hematuria_intensities[600]
        hematuria_red = hematuria_intensities[650]

        supply_mass = supply_weight_sensor.read(replicates=SUPPLY_WEIGHT_SENSOR_REPLICATES)
        waste_mass = waste_weight_sensor.read(replicates=WASTE_WEIGHT_SENSOR_REPLICATES)

        data = {
            'hematuria_purple': hematuria_purple,
            'hematuria_blue': hematuria_blue,
            'hematuria_green': hematuria_green,
            'hematuria_yellow': hematuria_yellow,
            'hematuria_orange': hematuria_orange,
            'hematuria_red': hematuria_red,
            'supply_mass': supply_mass,
            'waste_mass': waste_mass
        }
        add_data(data=data, file='sensor')

if __name__ == '__main__':
    sensor()
