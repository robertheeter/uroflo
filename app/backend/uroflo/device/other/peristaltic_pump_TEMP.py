'''
PERISTALTIC PUMP

About
- 

For
- Inflow rate control

Notes
- Pin allocation:
  PIN 33 (GPIO 13), PIN 35 (GPIO 19), PIN 37 (GPIO 26), PIN 39 (Ground)

Documentation
- 

'''

import numpy as np
import RPi.GPIO as GPIO


class PeristalticPump():
    def __init__(self):
        pass
    GPIO.setmode(GPIO.BOARD) # BOARD mode