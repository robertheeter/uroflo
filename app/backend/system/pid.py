'''
PID

Notes
- 500 mL water in container

Documentation

For tuning:
https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=9013

'''
import time
from simple_pid import PID
from components.spectral_sensor import SpectralSensor
from components.linear_actuator import LinearActuator

INFLOW_LEVEL_ADJUST_LIMIT = 15
INFLOW_ADJUSTMENT_SIZE = 0.005
HEMATURIA_SETPOINT = 0.5

Kp = 1
Ki = 0.1
Kd = 0.05

linear_actuator = LinearActuator(en_pin=10, in1_pin=9, in2_pin=11, freq=1000)
spectral_sensor = SpectralSensor(led_pin=4, use_led=True, sensor_type='VIS', max=48000)

pid = PID(Kp, Ki, Kd, setpoint=HEMATURIA_SETPOINT, output_limits=(0, INFLOW_LEVEL_ADJUST_LIMIT))
pid.sample_time = 1 # sample every 1 second


def get_hematuria():
    w_violet = -721.729
    b_violet = 1367.9
    w_blue = -24.4198
    b_blue = 944.002
    w_green = -374112
    b_green = -52082.8
    w_yellow = 40.1613
    b_yellow = 2405.44
    w_orange = 264983
    b_orange = -1684.04
    w_red = -81318.9
    b_red = -9016.87

    intensities = spectral_sensor.read(replicates=20)
    x_violet = intensities[450]
    x_blue = intensities[500]
    x_green = intensities[550]
    x_yellow = intensities[570]
    x_orange = intensities[600]
    x_red = intensities[650]

    hematuria = w_violet*(1/(x_violet - b_violet)) + w_blue*(1/(x_blue - b_blue)) + w_green*(1/(x_green - b_green)) + w_yellow*(1/(x_yellow - b_yellow)) + w_orange*(1/(x_orange - b_orange)) + w_red*(1/(x_red - b_red))
    return hematuria
    


while True:
    hematuria_percent = get_hematuria()
    print(hematuria_percent)

    # inflow_level_adjust = round(pid(hematuria_percent))
    
    # if inflow_level_adjust > 0:
    #     for _ in range(inflow_level_adjust):
    #         linear_actuator.retract(duty_cycle=100, duration=INFLOW_ADJUSTMENT_SIZE)
    # elif inflow_level_adjust < 0:
    #     for _ in range(abs(inflow_level_adjust)):
    #         linear_actuator.extend(duty_cycle=100, duration=INFLOW_ADJUSTMENT_SIZE)



