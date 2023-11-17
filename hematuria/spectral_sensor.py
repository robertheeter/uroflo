'''
Documentation
https://docs.circuitpython.org/projects/as726x/en/latest/api.html#adafruit_as726x.AS726x.read_calibrated_value

Python GitHub
https://github.com/adafruit/Adafruit_CircuitPython_AS726x

Visible Datasheet
https://cdn.sparkfun.com/assets/f/b/c/c/f/AS7262.pdf?_gl=1*12hia0d*_ga*ODIxNjU4Nzk4LjE3MDAyMDk5MjU.*_ga_T369JS7J9N*MTcwMDIwOTkyNS4xLjAuMTcwMDIwOTkyNS42MC4wLjA.

NIR Datasheet
https://cdn.sparkfun.com/assets/1/b/7/3/b/AS7263.pdf?_gl=1*1v54ztc*_ga*ODIxNjU4Nzk4LjE3MDAyMDk5MjU.*_ga_T369JS7J9N*MTcwMDIwOTkyNS4xLjEuMTcwMDIxMDM2NS42MC4wLjA.

Arduino GitHub
https://github.com/adafruit/Adafruit_AS726x/tree/master

'''

import time
import board

from adafruit_as726x import AS726x_I2C

sensor_type = 'VIS'

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = AS726x_I2C(i2c)
sensor.conversion_mode = sensor.MODE_2

print('Temperature: {0}C'.format(sensor.temperature))

while True:

    # wait for sensor to be ready
    while not sensor.data_ready:
        time.sleep(1)

    print("\n")
    if sensor_type == 'VIS':
        print("V: " + sensor.violet) # 450 nm
        print("B: " + sensor.blue) # 500 nm
        print("G: " + sensor.green) # 550 nm
        print("Y: " + sensor.yellow) # 570 nm
        print("O: " + sensor.orange) # 600 nm
        print("R: " + sensor.red) # 650 nm

    elif sensor_type == 'NIR':
        print("610: " + sensor.violet) # 610 nm
        print("680: " + sensor.blue) # 680 nm
        print("730: " + sensor.green) # 730 nm
        print("760: " + sensor.yellow) # 760 nm
        print("810: " + sensor.orange) # 810 nm
        print("860: " + sensor.red) # 860 nm

    time.sleep(1)
