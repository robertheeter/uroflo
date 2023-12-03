import time
# import sys
import RPi.GPIO as GPIO
from statistics import mean
from .hx711 import HX711

class Scale:
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
        print("Tare done! Add weight now...")

    def read_weight(self):
        weight = max(0, int(self.hx.get_weight(5)))
        self.hx.power_down()
        self.hx.power_up()
        time.sleep(0.1)
        return weight
    
#    def calculate_flow_rate(self, freq=60):
#        start_time = time.time()
#        current_time = time.time()

#        start_weight = 0
#        end_weight = 0
#        weights = []
#        calculate_start_weight = False

        # calculate flow rate once every cycle (set by frequency)
#        while current_time - start_time <= freq:
#            current_time = time.time()
#            reading = self.read_weight() # gets weight reading from hx711

#            if current_time - start_time <= 1:
#                weights.append(reading)
                
#            if current_time - start_time > 1 and not calculate_start_weight:
#                start_weight = mean(weights)
#                weights = []
#                calculate_start_weight = True

#            if current_time - start_time >= freq - 1 and current_time - start_time < freq:
#                weights.append(reading)

#            if current_time - start_time >= freq:
#                end_weight = mean(weights)
#                weight_change = start_weight - end_weight
#                flow_rate = (weight_change/(current_time - start_time))*60
#                return flow_rate
        
    def stop(self):
        print('Stopped')
        GPIO.cleanup()
        # sys.exit()
