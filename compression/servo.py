'''
SERVO

About
- 35 kg high torque servo motor (180° range)

Notes
- Recommend duty = (angle/20) + 2

Documentation
- Guide: https://www.instructables.com/Servo-Motor-Control-With-Raspberry-Pi/

'''

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # set up GPIO PWM pin
GPIO.setup(4, GPIO.OUT)

pwm = GPIO.PWM(4, 50)
pwm.start(0)


# duty = 2
# while duty <= 17:
# 	print(duty)
# 	pwm.ChangeDutyCycle(duty)
# 	time.sleep(1)
# 	duty += 1	

def SetAngle(angle):
	print(f"angle: {angle}")
	duty = (angle/20) + 2

	GPIO.output(4, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(4, False)
	pwm.ChangeDutyCycle(0)

max_angle = 220
max_flow = 10

while True:
	try:
		flow = input(f"Flow [0 to {max_flow}]: ")
		if flow == 'q':
			break
		flow = float(flow)
		if flow < 0 or flow > max_flow:
			raise Exception
	except:
		print("ERROR: Must be a number between 0 and 10.")
		continue
	
	angle = max_angle*flow/max_flow
	SetAngle(angle)

	
# for i in range(20):
# 	i = i*10
# 	SetAngle(i)
# 	time.sleep(1)
# SetAngle(0) # 0 is completely open
# time.sleep(2)
# SetAngle(180)
# time.sleep(2)
# SetAngle(90)
# time.sleep(2)
# SetAngle(180)
# time.sleep(2)
# SetAngle(0)

# time.sleep(2)

pwm.stop()

GPIO.cleanup()
    
    



