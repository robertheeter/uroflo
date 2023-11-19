'''
LINEAR ACTUATOR
- L298N driver
- 12 V linear actuator (1.2 in stroke, 0.6 in/s, 60 N / 14 lb)

Documentation
https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

'''

import RPi.GPIO as GPIO
import time

class LinearActuator():
    def __init__(self, pins=[23, 24, 25], freq=1000, verbose=False):
        self.in1 = pins[0]
        self.in2 = pins[1]
        self.en = pins[2]
        self.freq = freq
        self.verbose = verbose
        self.setup()

    def setup(self):
        if self.verbose:
            print(f"LinearActuator: pin in1 = {self.in1}")
            print(f"LinearActuator: pin in2 = {self.in2}")
            print(f"LinearActuator: pin en = {self.en}")
            print(f"LinearActuator: freq = {self.freq}")

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)

        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

        self.pwm = GPIO.PWM(self.en, self.freq)
        self.pwm.start(100)
    
    def run(self, dir='forward', speed=100, dur=-1):
        if dir not in ['forward', 'backward']:
            raise Exception("LinearActuator: dir must be 'forward' or 'backward'")

        if (speed < 0) or (speed > 100):
            raise Exception("LinearActuator: speed must be in [0, 100]")
        
        self.pwm.ChangeDutyCycle(speed)

        if dir == 'forward':
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)

        elif dir == 'backward':
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)

        if self.verbose:
            print(f"LinearActuator: dir = {dir}, speed = {speed}, dur = {dur}")

        if dur > 0:
            time.sleep(dur)
            self.stop()

    def stop(self):
        print(f"LinearActuator: stop")
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

la = LinearActuator(pins=[23, 24, 25], freq=1000, verbose=True)
la.run('backward', 101, 2)
la.run('forward', 100, 4)
la.run('backward', 60, 4)
la.run('forward', 60)
time.sleep(10)
la.stop()
