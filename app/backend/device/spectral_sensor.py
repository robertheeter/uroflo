'''
SPECTRAL SENSOR

About
- AS7262 (visible) or AS7263 (near-infrared) spectral sensor using I2C

For
- Hematuria severity measurement

Notes
- Recommend max = 48000 (VIS) or 16000 (NIR)
- Recommend replicates = 10
- Pin allocation:
  PIN 1 (3.3 V), PIN 3 (I2C SDA), PIN 5 (I2C SCL), PIN 7 (GPIO 4),
  PIN 9 (Ground)

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
    def __init__(self, led_pin, use_led=True, sensor_type='VIS', max=48000, verbose=False):
        self.led_pin = led_pin # GPIO LED pin (BCM)
        self.use_led = use_led # toggles whether to use LED when scanning
        self.sensor_type = sensor_type # type of AS726x sensor ('AS7262'/'VIS' or 'AS7263'/'NIR')
        
        self.MAX = max # maximum sensor scan intensity

        self.verbose = verbose # toggles printing of information to terminal

        self.setup()

    def setup(self):
        print("SpectralSensor: setup")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) # BCM mode

        i2c = board.I2C() # set up I2C; uses board.SCL and board.SDA
        self.sensor = AS726x_I2C(i2c)
        self.sensor.conversion_mode = self.sensor.MODE_2 # continuously gather samples/readings

        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.output(self.led_pin, GPIO.HIGH) # turn off LED
        
        self.check_temperature()

        if not self.sensor.data_ready:
            if self.verbose:
                print("SpectralSensor: data not ready; waiting...")
            time.sleep(0.5)
    
    def check_temperature(self):
        if self.verbose:
            print("SpectralSensor: temperature = {0}°C".format(self.sensor.temperature))

        if (self.sensor.temperature < 10) or (self.sensor.temperature > 40):
            raise Exception("SpectralSensor: temperature too hot (>40°C) or cold (<10°C)'")
        
    # set parameters
    def set_max(self, new_max):
        if self.verbose:
            print(f"SpectralSensor: set_max (new_max = {new_max})")
        self.MAX = new_max

    # scan raw intensities
    def scan(self):
        if self.use_led == True:
            GPIO.output(self.led_pin, GPIO.LOW) # turn on LED
        
        else:
            GPIO.output(self.led_pin, GPIO.HIGH) # turn off LED
        
        time.sleep(0.1)
        intensities = [self.sensor.violet, self.sensor.blue, self.sensor.green, self.sensor.yellow, self.sensor.orange, self.sensor.red] # get raw values with LED
        time.sleep(0.3)
        GPIO.output(self.led_pin, GPIO.HIGH) # turn off LED

        scan = []
        for intensity in intensities:
            scan.append(min(self.MAX, intensity)) # cap maximum sensor scan intensity

        return scan # return scanned intensities

    # read wavelength intensities
    def read(self, replicates=10):
        self.check_temperature()
        
        intensities = []
        for _ in range(replicates):
            intensities.append(self.scan())
            time.sleep(0.1)
        
        intensities = np.median(np.array(intensities), axis=0) # get median intensities across replicates

        if self.sensor_type in ['VIS', 'AS7262']:
            wavelengths = [450, 500, 550, 570, 600, 650] # visible channel wavelengths (AS7262)
        elif self.sensor_type in ['NIR', 'AS7263']:
            wavelengths = [610, 680, 730, 760, 810, 860] # near-infrared channel wavelengths (AS7263)

        reading = dict(zip(wavelengths, intensities))
        
        if self.verbose:
            print(f"SpectralSensor: reading = {reading} (replicates = {replicates})")
        
        return reading # return reading as a dictionary, where keys are wavelengths and values are median intensities
    
    def shutdown(self):
        print(f"SpectralSensor: shutdown")
        GPIO.output(self.led_pin, GPIO.HIGH) # turn off LED
        GPIO.cleanup()


# calibration testing
def calibrate():
    spectral_sensor = SpectralSensor(led_pin=4, use_led=True, sensor_type='VIS', max=48000, verbose=False)
    
    n = 20
    reading = spectral_sensor.read(replicates=n)

    print(reading)

    # trials = []
    # for i in range(n):
    #     readings = []
    #     for j in range(10):
    #         readings.append(ss.read(use_led=True))
    #         time.sleep(0.1)
        
    #     df = pd.DataFrame(readings)
    #     avg_readings = dict(df.mean())
    #     trials.append(avg_readings)
    
    # df = pd.DataFrame(trials)
    # avg_trials = dict(df.mean())

    print(f"\nAVERAGE READINGS (n={n}):\n")

    print('450 nm / violet : {:.2f}'.format(reading[450]))
    print('500 nm / blue   : {:.2f}'.format(reading[500]))
    print('550 nm / green  : {:.2f}'.format(reading[550]))
    print('570 nm / yellow : {:.2f}'.format(reading[570]))
    print('600 nm / orange : {:.2f}'.format(reading[600]))
    print('650 nm / red    : {:.2f}'.format(reading[650]))


    # df = pd.DataFrame(trials)
    # cov_trials = dict(df.std()/df.mean())

    # print(f"\nCOEFFICIENT OF VARIATION READINGS (n={n}):\n")

    # print('450 nm / violet : {:.4f}%'.format(cov_trials[450]*100))
    # print('500 nm / blue   : {:.4f}%'.format(cov_trials[500]*100))
    # print('550 nm / green  : {:.4f}%'.format(cov_trials[550]*100))
    # print('570 nm / yellow : {:.4f}%'.format(cov_trials[570]*100))
    # print('600 nm / orange : {:.4f}%'.format(cov_trials[600]*100))
    # print('650 nm / red    : {:.4f}%'.format(cov_trials[650]*100))
    
    # print("\n####################")
    # print(f"\nSTANDARD DEVIATION READINGS (n={n}):\n{df.std()}")
    # print(f"\nVARIANCE READINGS (n={n}):\n{df.var()}\n")




# example implementation
if __name__ == '__main__':
    # spectral_sensor = SpectralSensor(led_pin=4, use_led=True, sensor_type='VIS', max=48000, verbose=True) # use GPIO numbering (NOT pin numbering)
    # time.sleep(2) # wait for setup

    # spectral_sensor.read(replicates=10)

    # spectral_sensor.shutdown()
    
    calibrate()