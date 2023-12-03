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
    def __init__(self, pd_sck_pin=2, dout_pin=3):
        self.pd_sck_pin = pd_sck_pin
        self.dout_pin = dout_pin
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        self.hx = HX711(self.pd_sck_pin, self.dout_pin)
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(-242.22)
        self.hx.reset()
        self.hx.tare()
        print("WeightSensor: setup")

    def volume(self):
        weight = max(0, int(self.hx.get_weight(5)))
        self.hx.power_down()
        self.hx.power_up()
        time.sleep(0.1)
        print(f"WeightSensor: volume = {weight} mL")
        return weight
    
    def rate(self, interval=60):
        start_time = time.time()
        duration = 0

        start_weight = 0
        end_weight = 0
        weights = []
        calculate_start_weight = True

        while duration <= interval:
            duration = time.time() - start_time
            weight = self.read_weight()

            if duration <= 1:
                weights.append(weight)
                
            elif duration > 1 and calculate_start_weight:
                start_weight = np.mean(weights)
                weights = []
                calculate_start_weight = False

            elif duration >= interval - 1:
                weights.append(weight)

            elif duration >= interval:
                end_weight = np.mean(weights)
                rate = ((start_weight - end_weight)/duration)*60
                print(f"WeightSensor: rate = {rate} mL/min")
                return rate
        
    def stop(self):
        GPIO.cleanup()
        print("WeightSensor: stop")
