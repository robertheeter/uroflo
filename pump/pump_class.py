class Pump:
    def __init__(self, motor):
        '''
        Initializes motor object with initial speed of 20 mL/min.
        '''
        self.motor = motor
        self.flow_rate = 20
        self.speed = flow_to_speed(self.flow_rate)

    def __str__(self):
        return (f'Pump is currently running at {self.flow_rate} mL/min')

    def accelerate(self, target_flow_rate):
        '''
        Accelerates/decelerates motor from current flow rate to a target flow rate.

        Input: target_flow_rate (mL/min)
        '''
        self.flow_rate = target_flow_rate
        target_speed = flow_to_speed(target_flow_rate)
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
        print(f'Running at {self.flow_rate} for {time} seconds')
        total_steps = int(time/(2*self.speed))
        self.motor.motor_go(False, "Full", total_steps, self.speed, False, 0)

    def stop(self):
        '''
        Stops motor.
        '''
        print('Stopping motor')
        self.motor.motor_stop()


def flow_to_speed(flow_rate):
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