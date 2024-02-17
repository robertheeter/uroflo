'''
PERISTALTIC PUMP

Notes:
- For inflow rate control

- Pin allocation:
  PIN 33 (GPIO 13), PIN 35 (GPIO 19), PIN 37 (GPIO 26), PIN 39 (Ground)

Documentation
- 

'''

import numpy as np
import RPi.GPIO as GPIO
import os
import time


class PeristalticPump():
    def __init__(self, verbose=False):
        pass
  
    def setup(self):
        print("PeristalticPump: setup")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) # BCM mode

        pass
    
    def shutdown(self):
        print(f"PeristalticPump: shutdown")
        GPIO.cleanup()


# example implementation
if __name__ == '__main__':
    os.chdir("../device") # change current directory
    peristaltic_pump = PeristalticPump(verbose=True) # use GPIO numbering (NOT pin numbering)
    time.sleep(2) # wait for setup

    peristaltic_pump.shutdown()
