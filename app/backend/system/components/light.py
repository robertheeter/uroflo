'''
LIGHT

Notes
- For notification system

- LED strip light using 3 R, G, and B N-channel MOSFETs

- Pin allocation:
  PIN 24 (GPIO 8) [RED], PIN 26 (GPIO 7) [GREEN], PIN 28 (GPIO 1) [BLUE], PIN 30 (Ground) [BLACK]

Documentation
- Guide: https://learn.adafruit.com/rgb-led-strips

'''

import time
import board
import RPi.GPIO as GPIO
import os


class Light():
    def __init__(self, red_pin, green_pin, blue_pin, verbose=False):
        self.red_pin = red_pin # GPIO red pin (BCM)
        self.green_pin = green_pin # GPIO green pin (BCM)
        self.blue_pin = blue_pin # GPIO blue pin (BCM)

        self.verbose = verbose

        self.setup()

    def setup(self):
        print("Light: setup")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) # BCM mode

        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        # GPIO.setup(self.blue_pin, GPIO.OUT) # not using blue color

        GPIO.output(self.red_pin, GPIO.LOW) # turn off color
        GPIO.output(self.green_pin, GPIO.LOW) # turn off color
        # GPIO.output(self.blue_pin, GPIO.LOW) # turn off color; not using blue color

    # set LED light to color
    def color(self, color):
        if color not in ['off', 'green', 'yellow', 'red']:
            raise Exception(f"Light: color = {color} not available")
        
        if self.verbose:
            print(f"Light: color (color = {color})")
        
        if color == 'off':
            GPIO.output(self.red_pin, GPIO.LOW) # turn off color
            GPIO.output(self.green_pin, GPIO.LOW) # turn off color
            # GPIO.output(self.blue_pin, GPIO.LOW) # turn off color; not using blue color
            
        elif color == 'green':
            GPIO.output(self.red_pin, GPIO.LOW) # turn off color
            GPIO.output(self.green_pin, GPIO.HIGH) # turn on color
            # GPIO.output(self.blue_pin, GPIO.LOW) # turn off color; not using blue color

        elif color == 'yellow':
            GPIO.output(self.red_pin, GPIO.HIGH) # turn on color
            GPIO.output(self.green_pin, GPIO.HIGH) # turn on color
            # GPIO.output(self.blue_pin, GPIO.LOW) # turn off color; not using blue color

        elif color == 'red':
            GPIO.output(self.red_pin, GPIO.HIGH) # turn on color
            GPIO.output(self.green_pin, GPIO.LOW) # turn off color
            # GPIO.output(self.blue_pin, GPIO.LOW) # turn off color; not using blue color

    def shutdown(self):
        print("Light: shutdown")
        self.color(color='off')
        GPIO.cleanup()


# example implementation
if __name__ == '__main__':
    os.chdir('..') # change current directory
    
    light = Light(red_pin=board.D8, green_pin=board.D7, blue_pin=board.D1, verbose=True) # use BOARD.D[GPIO] numbering (BCM) (NOT pin numbering)
    time.sleep(2) # wait for setup

    for color in ['green', 'yellow', 'off', 'red']:
        light.color(color=color)
        time.sleep(4)
    
    light.shutdown()