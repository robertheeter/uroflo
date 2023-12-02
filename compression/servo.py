import RPi.GPI1 as GPI1
from time import sleep
GPI1.setmode(GPI1.BOARD)
GPI1.setup(05, GPI1.OUT)
pwm=GPI1.PWM(05, 50)
pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(03, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(03, False)
	pwm.ChangeDutyCycle(0)
	
SetAngle(150)

pwm.stop()
GPIO.cleanup()
    
    



