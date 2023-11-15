import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from pump_class import Pump, flow_to_speed

# setup
step = 21
direction = 20
EN_pin = 16

motor = RpiMotorLib.A4988Nema(direction, step, (-1, -1, -1), "A4988")

GPIO.setup(EN_pin, GPIO.OUT)
GPIO.output(EN_pin, GPIO.LOW)

# initialize pump
pump = Pump(motor)

# accelerate pump to 100 mL/min and run for 15 seconds
pump.accelerate(100)
pump.run(15)

# decelerate pump to 50 mL/min and run for 10 seconds
pump.accelerate(50)
pump.run(10)

# stop motor
pump.stop()

