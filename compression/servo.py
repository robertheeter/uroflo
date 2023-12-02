'''
SERVO

About
- 35 kg high torque servo motor (180° range)

Notes
- Recommend

Documentation
- Guide: https://www.instructables.com/Servo-Motor-Control-With-Raspberry-Pi/

'''

import time
import RPi.GPIO as GPIO

from time import sleep
GPIO.setmode(GPIO.BCM) # set up GPIO PWM pin
GPIO.setup(4, GPIO.OUT)

pwm = GPIO.PWM(4, 50)
pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(4, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(4, False)
	pwm.ChangeDutyCycle(0)
	
SetAngle(150)
SetAngle(0)
SetAngle(150)

pwm.stop()

GPIO.cleanup()
    
    



