'''
PERISTALTIC PUMP

About
- 

For
- Inflow rate control

Notes
- Pin allocation (use 'GPIO.setmode(GPIO.BOARD)'):
  PIN 33 (GPIO), PIN 35 (GPIO), PIN 37 (GPIO), PIN 39 (Ground)

Documentation
- 

'''

import numpy as np
import RPi.GPIO as GPIO


class PeristalticPump():
    def __init__(self):
        pass
    GPIO.setmode(GPIO.BOARD) # BOARD mode