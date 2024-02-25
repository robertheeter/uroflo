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

import csv

INFLOW_LEVEL_ADJUST_LIMIT = 5
INFLOW_ADJUSTMENT_SIZE = 0.005
HEMATURIA_SETPOINT = 0.4

Kp = -1
Ki = -0.01
Kd = -0.05


pid = PID(Kp, Ki, Kd, setpoint=HEMATURIA_SETPOINT, output_limits=(-1*INFLOW_LEVEL_ADJUST_LIMIT, INFLOW_LEVEL_ADJUST_LIMIT))
#pid.sample_time = 5 # sample every 10 seconds

percent = ['percent']
adjustment = ['adjustment']
hematuria_readings = [6.2, 5.5, 5.1, 3.4, 2.3, 0.9, 0.1, 0.1, 0.1, 0.1, 0.9, 1.6, 3.6, 4.9]

for hematuria_percent in hematuria_readings:
    
    percent.append(hematuria_percent)

    print(f"hematuria percent: {hematuria_percent}%")

    inflow_level_adjust = round(pid(hematuria_percent))
    
    print(f"inflow level adjust: {inflow_level_adjust}")

    adjustment.append(inflow_level_adjust)

    p, i, d = pid.components
    
    print(f"p: {p:.2f}, i: {i:.2f}, d: {d:.2f}\n")

    time.sleep(5)


data_set = [percent, adjustment]

# Transpose the data to convert columns to rows
data_rows = zip(*data_set)

# Specify the file name
file_name = "PID_TESTING_2.csv"

# Writing the transposed data to a CSV file
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_rows)

print("CSV file has been created successfully:", file_name)
