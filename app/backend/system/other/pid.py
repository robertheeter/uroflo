'''
PID

Notes
- 

Documentation

For tuning:
https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=9013

'''
import time
from simple_pid import PID


def get_hematuria(idx):
    levels = list(range(46, 58, 2))
    levels.extend(list(reversed(range(46, 58, 2))))
    return levels[idx]


Kp = 1
Ki = 0.1
Kd = 0.05
hematuria_setpoint = 56

pid = PID(Kp, Ki, Kd, setpoint=hematuria_setpoint, output_limits=(0, 15))
# use output_limits to contrain the output to a range


# set sample time to have updates every 1 second (allow enough time for response)
# (note that this doesn't stop the loop it is in, pid has internal timing for that)
pid.sample_time = 1

i = 0

while True:
    # Compute new output from the PID according to the systems current value
    h = get_hematuria(i)
    control = pid(h)

    print(f'Hematuria: {h}, Control: {control}')
#    time.sleep(1)
    print(i)
    i += 1
