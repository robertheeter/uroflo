'''
WEIGHT SENSOR

About
- HX711 weight sensor using IC

Notes
- 

Documentation
- 

'''

import time
import RPi.GPIO as GPIO
import numpy as np
from .hx711 import HX711

class WeightSensor():
    def __init__(self, pd_sck_pin=2, dout_pin=3, verbose=False):
        self.pd_sck_pin = pd_sck_pin # GPIO SKC pin
        self.dout_pin = dout_pin # GPIO DOUT pin
        self.verbose = verbose # toggles printing of information to terminal
        self.setup()

    def setup(self):
        print("WeightSensor: setup")
        GPIO.setwarnings(False)
        self.hx = HX711(self.pd_sck_pin, self.dout_pin)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(-242.22)
        self.hx.reset()
        self.hx.tare()

    def mass(self):
        mass = max(0, int(self.hx.get_weight(5)))
        self.hx.power_down()
        self.hx.power_up()
        time.sleep(0.1)
        if self.verbose:
            print(f"WeightSensor: mass = {mass} mg")
        return mass
    
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
        
    def stop(self):
        print("WeightSensor: stop")
        GPIO.cleanup()
