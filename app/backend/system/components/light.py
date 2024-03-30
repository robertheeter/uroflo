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
import pwmio
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
        self.red = pwmio.PWMOut(self.red_pin)
        self.green = pwmio.PWMOut(self.green_pin)
        self.blue = pwmio.PWMOut(self.blue_pin)

    # convert between percent and duty_cycle
    def duty_cycle(self, percent):
        return int(percent / 100.0 * 65535.0)

    # set LED light to color
    def color(self, color):
        if color not in ['off', 'default', 'yellow', 'orange', 'red']:
            raise Exception(f"Light: color = {color} not available")
        
        if self.verbose:
            print(f"Light: color (color = {color})")
        
        if color == 'off':
            self.red.duty_cycle = self.duty_cycle(0)
            self.green.duty_cycle = self.duty_cycle(0)
            self.blue.duty_cycle = self.duty_cycle(0)
        
        elif color == 'default':
            self.red.duty_cycle = self.duty_cycle(1)
            self.green.duty_cycle = self.duty_cycle(2.74)
            self.blue.duty_cycle = self.duty_cycle(4)
            
        elif color == 'yellow':
            self.red.duty_cycle = self.duty_cycle(20)
            self.blue.duty_cycle = self.duty_cycle(0)
            self.green.duty_cycle = self.duty_cycle(10)

        elif color == 'orange':
            self.red.duty_cycle = self.duty_cycle(50)
            self.blue.duty_cycle = self.duty_cycle(0)
            self.green.duty_cycle = self.duty_cycle(10)

        elif color == 'red':
            self.red.duty_cycle = self.duty_cycle(50)
            self.blue.duty_cycle = self.duty_cycle(0)
            self.green.duty_cycle = self.duty_cycle(0)

    def shutdown(self):
        print("Light: shutdown")
        self.color(color='off')
        self.red.deinit()
        self.green.deinit()
        self.blue.deinit()


# example implementation
if __name__ == '__main__':
    os.chdir('..') # change current directory
    
    light = Light(red_pin=board.D8, green_pin=board.D7, blue_pin=board.D1, verbose=True) # use BOARD.D[GPIO] numbering (BCM) (NOT pin numbering)
    time.sleep(2) # wait for setup

    for color in ['default', 'off', 'yellow', 'orange', 'red']:
        light.color(color=color)
        time.sleep(4)
    
    light.shutdown()