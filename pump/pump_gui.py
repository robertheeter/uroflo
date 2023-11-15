import time
from guizero import App, Slider
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

# setup
step = 21
direction = 20
EN_pin = 16

pump = RpiMotorLib.A4988Nema(direction, step, (-1, -1, -1), "A4988")

GPIO.setup(EN_pin, GPIO.OUT)
GPIO.output(EN_pin, GPIO.LOW)

def flow_to_speed(target_flow):
	# convert flow rate to rpm
	target_rpm = (3.149*target_flow) + 21.09

	# convert rpm to speed (time delay between motor steps)
	target_speed = 60/(200*target_rpm)
	return target_speed


def accelerate(start_speed, target_speed):
	speed = start_speed
	steps = 120
	delta_speed = 0.0001

	if start_speed > target_speed:
		print('Accelerating')
		while speed > target_speed:
			pump.motor_go(False, "Full", steps, speed, False, 0)
			speed -= delta_speed
	else:
		print('Decelerating')
		while speed < target_speed:
			pump.motor_go(False, "Full", steps, speed, False, 0)
			speed += delta_speed


def run(target_speed, time):
	print(f'Running for {time} seconds')
	total_steps = int(time/(2*target_speed))
	pump.motor_go(False, "Full", total_steps, target_speed, False, 0)



# START VALUES
start_flow_rate = 20 # DO NOT CHANGE
target_flow_rate = 80 # ADJUST THIS (mL/min)

start_speed = flow_to_speed(start_flow_rate)
target_speed = flow_to_speed(target_flow_rate) # converts flow rate to speed

accelerate(start_speed, target_speed)
run(target_speed, 1)


# RUN MOTOR
previous_flow_rate = target_flow_rate
previous_speed = target_speed

def on_slider_change():
	global previous_flow_rate
	global previous_speed

	target_flow_rate = int(slider.value)
	target_speed = flow_to_speed(target_flow_rate)

	if target_flow_rate != previous_flow_rate:
		accelerate(previous_speed, target_speed)

	run(target_speed, 5) # run for 1 second each loop

	previous_flow_rate = target_flow_rate
	previous_speed = target_speed
#	time.sleep(1) # wait for 1 second



app = App()

slider = Slider(app, start=20, end=100, width=200, height=50, command=on_slider_change)
slider.text_size = 15
slider.bg = "lightgray"

slider.when_changed = on_slider_change

app.display()

#new_flow_rate = 45
#new_speed = flow_to_speed(new_flow_rate)

#accelerate(target_speed, new_speed)
#run(new_speed, 5)
