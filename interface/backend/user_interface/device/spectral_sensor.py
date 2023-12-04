'''
SPECTRAL SENSOR

About
- AS7262 (visible) or AS7263 (near-infrared) spectral sensor using I2C

Notes
- Recommend reading max = 48000 (VIS) or 16000 (NIR)

Documentation
- Guide: https://learn.adafruit.com/adafruit-as7262-6-channel-visible-light-sensor
- CircuitPython Documentation: https://docs.circuitpython.org/projects/as726x/en/latest/api.html#adafruit_as726x.AS726x.read_calibrated_value
- CircuitPython GitHub: https://github.com/adafruit/Adafruit_CircuitPython_AS726x
- Arduino GitHub: https://github.com/adafruit/Adafruit_AS726x/tree/master
- Visible Datasheet: https://cdn.sparkfun.com/assets/f/b/c/c/f/AS7262.pdf?_gl=1*12hia0d*_ga*ODIxNjU4Nzk4LjE3MDAyMDk5MjU.*_ga_T369JS7J9N*MTcwMDIwOTkyNS4xLjAuMTcwMDIwOTkyNS42MC4wLjA.
- Near-Infrared Datasheet https://cdn.sparkfun.com/assets/1/b/7/3/b/AS7263.pdf?_gl=1*1v54ztc*_ga*ODIxNjU4Nzk4LjE3MDAyMDk5MjU.*_ga_T369JS7J9N*MTcwMDIwOTkyNS4xLjEuMTcwMDIxMDM2NS42MC4wLjA.

'''

import time
import board
import RPi.GPIO as GPIO
from adafruit_as726x import AS726x_I2C
import numpy as np

class SpectralSensor():
    def __init__(self, led_pin=4, sensor_type='VIS', max_scan=16000, verbose=False):
        GPIO.cleanup()
        self.led_pin = led_pin # GPIO LED pin (3.3V)
        self.sensor_type = sensor_type # type of AS726x sensor ('AS7262'/'VIS' or 'AS7263'/'NIR')
        self.max_scan = max_scan # maximum sensor scan intensity
        self.verbose = verbose # toggles printing of information to terminal
        self.setup()

    def setup(self):
        print("SpectralSensor: setup")
        if self.verbose:
            print(f"SpectralSensor: sensor_type = {self.sensor_type}")
            print(f"SpectralSensor: max_scan = {self.max_scan}")

        i2c = board.I2C() # set up I2C; uses board.SCL and board.SDA
        self.sensor = AS726x_I2C(i2c)
        self.sensor.conversion_mode = self.sensor.MODE_2 # continuously gather samples/readings

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) # set up GPIO LED pin
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH) # turn off LED
        
        if self.verbose:
            print("SpectralSensor: temperature = {0}°C".format(self.sensor.temperature))

        if (self.sensor.temperature < 10) or (self.sensor.temperature > 40):
            raise Exception("SpectralSensor: temperature too hot (>30°C) or cold (<18°C)'")

        if not self.sensor.data_ready:
            if self.verbose:
                print("SpectralSensor: data not ready; waiting...")
            time.sleep(1)
    
    def scan(self, use_led=True):
        if use_led == True:
            GPIO.output(self.led_pin, GPIO.LOW) # turn on LED
            time.sleep(0.3)
            intensities = [self.sensor.violet, self.sensor.blue, self.sensor.green, self.sensor.yellow, self.sensor.orange, self.sensor.red] # get raw values with LED
            time.sleep(0.3)
            GPIO.output(self.led_pin, GPIO.HIGH) # turn off LED

        else:
            GPIO.output(self.led_pin, GPIO.HIGH) # turn off LED
            time.sleep(0.3)
            intensities = [self.sensor.violet, self.sensor.blue, self.sensor.green, self.sensor.yellow, self.sensor.orange, self.sensor.red] # get raw values without LED
            time.sleep(0.3)
        
        scan = []
        for intensity in intensities:
            scan.append(min(self.max_scan, intensity)) # cap maximum sensor scan intensity

        return scan # return scanned intensities

    def read(self, n=5):
        if self.verbose:
            print("SpectralSensor: temperature = {0}°C".format(self.sensor.temperature))

        if (self.sensor.temperature < 10) or (self.sensor.temperature > 40):
            raise Exception("SpectralSensor: temperature too hot (>30°C) or cold (<18°C)'")
        
        intensities = []
        for i in range(n):
            intensities.append(self.scan(use_led=True))
            time.sleep(0.1)
        
        print(np.array(intensities))
        intensities = np.mean(np.array(intensities), axis=0) # average n scans to get intensity

        if self.sensor_type in ['VIS', 'AS7262']:
            wavelengths = [450, 500, 550, 570, 600, 650] # visible channel wavelengths (AS7262)
        elif self.sensor_type in ['NIR', 'AS7263']:
            wavelengths = [610, 680, 730, 760, 810, 860] # near-infrared channel wavelengths (AS7263)

        reading = dict(zip(wavelengths, intensities))

        if self.verbose:
            print(f"SpectralSensor: reading = {reading}")
        
        return reading # return reading as a dictionary, where keys are wavelengths and values are intensities averaged from n scans

    def level(self, weights, bias, max, n=5, range=[0, 100]):
        reading = self.read(n)
        intensities = reading.values()

        level = sum([w*i for w, i in zip(weights, intensities)]) + bias # apply least squares regression weights and bias to predict level

        rescaled_level = int((level/max * (range[1]-range[0])) + range[0])
        
        if self.verbose:
            print(f"SpectralSensor: level = {rescaled_level} in range [{range[0]}-{range[1]}]")

        return rescaled_level # return rescaled level
    
    def stop(self):
        print(f"SpectralSensor: stop")
        GPIO.output(self.led_pin, GPIO.HIGH) # turn off LED
        GPIO.cleanup()
