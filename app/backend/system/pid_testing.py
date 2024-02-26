'''
PID

Notes
- 500 mL water in container

Documentation

For tuning:
https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=9013

'''
import csv
import time
from simple_pid import PID
from matplotlib import pyplot as plt
import random

class BladderSimulation:
    def __init__(self, initial_hematuria=10, max_variation=0.65):
        self.hematuria = initial_hematuria
        self.max_variation = max_variation

    def update_hematuria(self, saline_flow_rate):
        # Simulate random variations in hematuria level
        variation = random.uniform(-self.max_variation, self.max_variation)
        self.hematuria += variation

        # Adjust hematuria based on saline inflow rate
        self.hematuria -= 0.4 * saline_flow_rate  # Adjust this formula as needed

        # Ensure hematuria stays within the valid range of 0 to 15%
        self.hematuria = max(0, min(15, self.hematuria))

    def get_hematuria(self):
        return self.hematuria

#    def adjust_saline_inflow(self):
        # Adjust saline inflow based on hematuria level
#        saline_flow_rate = 2 * self.hematuria  # Adjust this formula as needed
#        return saline_flow_rate


INFLOW_LEVEL_ADJUST_LIMIT = 2
INFLOW_ADJUSTMENT_SIZE = 0.005
HEMATURIA_SETPOINT = 0.5

Kp = -1
Ki = -0.01
Kd = -0.1

simulation = BladderSimulation()

pid = PID(Kp, Ki, Kd, setpoint=HEMATURIA_SETPOINT, output_limits=(-1*INFLOW_LEVEL_ADJUST_LIMIT, INFLOW_LEVEL_ADJUST_LIMIT))
#pid.sample_time = 5 # sample every 10 seconds 

percent = []

start = time.time()
while True:
    hematuria_percent = simulation.get_hematuria()
    inflow_level_adjust = pid(hematuria_percent)
    simulation.update_hematuria(inflow_level_adjust)
    
    p, i, d = pid.components
    print(f"hematuria percent: {hematuria_percent:.2f}%")
    print(f"inflow level adjust: {inflow_level_adjust:.2f}")
    print(f"p: {p:.2f}, i: {i:.2f}, d: {d:.2f}\n")

    percent.append(hematuria_percent)

    time.sleep(1)

    if time.time() - start > 30:
        break

x = list(range(len(percent)))
y = percent
plt.plot(x, y)
plt.xlabel('Time (s)')
plt.ylabel('Hematuria (%)')
plt.show()

