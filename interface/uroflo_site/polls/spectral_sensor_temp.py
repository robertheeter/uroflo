'''
SPECTRAL SENSOR

About
- AS7262 (visible) or AS7263 (near-infrared) spectral sensors using I2C

Notes
- Recommend reading max = 16000

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

# spectral sensor class
class SpectralSensor():
    def __init__(self, led_pin=4, sensor_type='VIS', range=[0, 100], max=16000, verbose=False):
        self.led_pin = led_pin # GPIO LED pin (3.3V)
        self.sensor_type = sensor_type # type of AS726x sensor ('AS7262'/'VIS' or 'AS7263'/'NIR')
        self.max = max # maximum sensor reading
        self.range = range # range of rescaled readings
        self.verbose = verbose # toggles printing of information to terminal
        self.setup()

    def setup(self):
        if self.verbose:
            print(f"SpectralSensor: sensor_type = {self.sensor_type}")
            print(f"SpectralSensor: reading max = {self.max}")
            print(f"SpectralSensor: reading range = {self.range}")

        i2c = board.I2C() # set up I2C; uses board.SCL and board.SDA
        self.sensor = AS726x_I2C(i2c)
        self.sensor.conversion_mode = self.sensor.MODE_2 # continuously gather samples/readings

        GPIO.setmode(GPIO.BCM) # set up GPIO LED pin
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH)
        
        if self.verbose:
            print("SpectralSensor: temperature = {0}°C".format(self.sensor.temperature))

        if (self.sensor.temperature < 10) or (self.sensor.temperature > 40):
            raise Exception("SpectralSensor: temperature too hot (>30°C) or cold (<18°C)'")

        if not self.sensor.data_ready:
            if self.verbose:
                print("SpectralSensor: data not ready; waiting...")
            time.sleep(1)

    def rescale(self, val, range, max):
        return min(int((val * (range[1] - range[0]) / max) + range[0]), range[1])
    
    def read(self, use_led=True):
        if self.verbose:
            print("SpectralSensor: temperature = {0}°C".format(self.sensor.temperature))

        if (self.sensor.temperature < 10) or (self.sensor.temperature > 40):
            raise Exception("SpectralSensor: temperature too hot (>30°C) or cold (<18°C)'")
        
        if use_led == True:
            GPIO.output(self.led_pin, GPIO.LOW) # turn on LED
            time.sleep(0.1)
            vals = [self.sensor.violet, self.sensor.blue, self.sensor.green, self.sensor.yellow, self.sensor.orange, self.sensor.red] # get raw values with LED
            GPIO.output(self.led_pin, GPIO.HIGH) # turn off LED

        else:
            GPIO.output(self.led_pin, GPIO.HIGH) # turn off LED
            time.sleep(0.1)
            vals = [self.sensor.violet, self.sensor.blue, self.sensor.green, self.sensor.yellow, self.sensor.orange, self.sensor.red] # get raw values without LED
        
        if self.verbose:
            print(f"SpectralSensor: reading raw vals = {vals}")
        
        rescaled_vals = []
        for val in vals:
            rescaled_val = self.rescale(val, self.range, self.max) # rescale raw values
            rescaled_vals.append(rescaled_val)

        if self.sensor_type in ['VIS', 'AS7262']:
            wavelengths = [450, 500, 550, 570, 600, 650] # visible channel wavelengths (AS7262)
        elif self.sensor_type in ['NIR', 'AS7263']:
            wavelengths = [610, 680, 730, 760, 810, 860] # near-infrared channel wavelengths (AS7263)

        readings = dict(zip(wavelengths, rescaled_vals))

        return readings # return readings as a dictionary, where keys are wavelengths and values are rescaled values

    def stop(self):
        print(f"SpectralSensor: stop")
        GPIO.output(self.led_pin, GPIO.HIGH)

# testing
if __name__ == '__main__':
    ss = SpectralSensor(led_pin=4, sensor_type='VIS', range=[0, 100], max=16000, verbose=True)

    for i in range(10):
        readings = ss.read(use_led=True)
        print(readings)
        time.sleep(1) # wait
