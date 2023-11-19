import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

class Pump:
    def __init__(self, step_pin=21, dir_pin=20, en_pin=16):
        '''
        Initializes motor object with initial speed of 20 mL/min.
        '''
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
        self.flow_rate = 20
        self.speed = self.flow_to_speed(self.flow_rate)
        self.setup()


    def setup(self):
        self.motor = RpiMotorLib.A4988Nema(self.dir_pin, self.step_pin, (-1, -1, -1), "A4988")
        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.output(self.en_pin, GPIO.LOW)


    def flow_to_speed(self, flow_rate):
        '''
        Converts flow rate to time delay between motor steps.

        Input: flow_rate (mL/min)
        Returns: speed (time delay between motor steps)
        '''
        # convert flow rate to rpm with linear regression model
        rpm = (3.149*flow_rate) + 21.09

        # convert rpm to speed
        speed = 60/(200*rpm)
        return speed


    def accelerate(self, target_flow_rate):
        '''
        Accelerates/decelerates motor from current flow rate to a target flow rate.

        Input: target_flow_rate (mL/min)
        '''
        self.flow_rate = target_flow_rate
        target_speed = self.flow_to_speed(target_flow_rate)
        initial_speed = self.speed
        steps = 120 # accelerate over 120 steps (0.6 revolutions)
        delta_speed = 0.0001

        if initial_speed > target_speed:
            print(f'Accelerating to {target_flow_rate} mL/min')
            while self.speed > target_speed:
                self.motor.motor_go(False, "Full", steps, self.speed, False, 0)
                self.speed -= delta_speed
        else:
            print(f'Decelerating to {target_flow_rate} mL/min')
            while self.speed < target_speed:
                self.motor.motor_go(False, "Full", steps, self.speed, False, 0)
                self.speed += delta_speed

    def run(self, time):
        '''
        Runs motor at the current flow rate for a specified time.

        Input: time (seconds)
        '''
        print(f'Running at {self.flow_rate} mL/min for {time} seconds')
        total_steps = int(time/(2*self.speed))
        self.motor.motor_go(False, "Full", total_steps, self.speed, False, 0)

    def stop(self):
        '''
        Stops motor.
        '''
        print('Stopping motor')
        self.motor.motor_stop()

