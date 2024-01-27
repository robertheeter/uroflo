'''
LINEAR ACTUATOR

About
- L298N driver
- 12 V linear actuator (1.2 in stroke, 0.6 in/s, 60 N / 14 lb)

Notes
- The linear actuator takes dur = 4.4-4.6 s at speed = 100 to extend or retract fully
- Recommend PWM freq = 1000

Documentation
- Guide: https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

'''

import time
import RPi.GPIO as GPIO

# linear actuator class
class LinearActuator():
    def __init__(self, pins=[10, 9, 11], freq=1000, verbose=False):
        self.en = pins[0] # GPIO enable pin
        self.in1 = pins[1] # GPIO input pin 1
        self.in2 = pins[2] # GPIO input pin 2
        self.freq = freq # PWM frequency
        self.verbose = verbose # toggles printing of information to terminal
        self.setup()

    def setup(self):
        if self.verbose:
            print(f"LinearActuator: pin in1 = {self.in1}")
            print(f"LinearActuator: pin in2 = {self.in2}")
            print(f"LinearActuator: pin en = {self.en}")
            print(f"LinearActuator: freq = {self.freq}")

        GPIO.setmode(GPIO.BCM) # set up GPIO pins

        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)

        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

        self.pwm = GPIO.PWM(self.en, self.freq) # start PWM
        self.pwm.start(100)
    
    def run(self, dir='forward', speed=100, dur=-1):
        if dir not in ['forward', 'backward']:
            raise Exception("LinearActuator: dir must be 'forward' or 'backward'")

        # if (speed < 25) or (speed > 100):
            # raise Exception("LinearActuator: speed must be in [25, 100]")
        
        self.pwm.ChangeDutyCycle(speed) # set speed via duty cycle

        if dir == 'forward':
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)

        elif dir == 'backward':
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)

        if self.verbose:
            print(f"LinearActuator: dir = {dir}, speed = {speed}, dur = {dur}")

        if dur > 0: # run continously lif dur <= 0
            time.sleep(dur) # wait for dur
            self.stop()

    def stop(self):
        print(f"LinearActuator: stop")
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

    def off(self):
        print(f"LinearActuator: off")
        GPIO.cleanup() # cleans GPIO

# testing
if __name__ == '__main__':
    la = LinearActuator(pins=[19, 21, 23], freq=1000, verbose=True)

    # la.run('backward', 1000, 10)
    time.sleep(2) # wait
    la.run('forward', 100, 10)
    time.sleep(2)
    la.run('backward', 25, 10)
    time.sleep(2)
    la.run('forward', 25, 10)

    time.sleep(1) # wait
    # la.run('backward', 60, 4)
    # time.sleep(1) # wait
    # la.run('forward', 60, 3)
    # time.sleep(1) # wait
    # la.run('forward', 60) # run continuously if dur <= 0
    # time.sleep(10) # wait
    la.stop()
    la.off()
