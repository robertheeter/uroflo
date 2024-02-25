'''
MASS

Notes
- Measures supply and waste bag masses and rate of mass change using weight sensors

Documentation
- See components/weight_sensor.py

'''

import time
import numpy as np
from sklearn.linear_model import LinearRegression

from data import *

from components.weight_sensor import WeightSensor


# sensor/script parameters
SUPPLY_WEIGHT_SENSOR_REPLICATES = 20
WASTE_WEIGHT_SENSOR_REPLICATES = 20
RATE_REPLICATES = 4 # number of weight measurements to use for each rate calculation
DELAY = 1 # delay between iterations

def mass():

    # instantiate weight sensors and linear regression
    supply_weight_sensor = WeightSensor(pdsck_pin=18, dout_pin=23, offset=1, scale=1)
    waste_weight_sensor = WeightSensor(pdsck_pin=14, dout_pin=15, offset=1, scale=1)

    regression = LinearRegression()

    # set lists to store previous supply and waste masses and times
    supply_masses = []
    supply_times = []
    waste_masses = []
    waste_times = []
    
    # run continuously
    i = 0
    while True:

        # get masses and timepoints
        supply_mass = supply_weight_sensor.read(replicates=SUPPLY_WEIGHT_SENSOR_REPLICATES)
        supply_time = time.time()
        waste_mass = waste_weight_sensor.read(replicates=WASTE_WEIGHT_SENSOR_REPLICATES)
        waste_time = time.time()
        
        supply_masses.insert(0, supply_mass)
        supply_times.insert(0, supply_time)
        waste_masses.insert(0, waste_mass)
        waste_times.insert(0, waste_time)

        # calculate rates with linear regression
        if i >= RATE_REPLICATES:
            supply_masses.pop() # remove old data
            supply_times.pop()
            waste_masses.pop()
            waste_times.pop()

            regression.fit(np.array(supply_times).reshape(-1, 1), np.array(supply_masses).reshape(-1, 1))
            supply_rate = regression.coef_

            regression.fit(np.array(waste_times).reshape(-1, 1), np.array(waste_masses).reshape(-1, 1))
            waste_rate = regression.coef_

        else:
            supply_rate = 0
            waste_rate = 0
            i += 1

        data = {
            'supply_mass': supply_mass,
            'supply_rate': supply_rate,
            'waste_mass': waste_mass,
            'waste_rate': waste_rate
        }

        add_data(data=data, file='mass')

        time.sleep(DELAY)

if __name__ == '__main__':
    mass()
