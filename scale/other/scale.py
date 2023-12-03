#!/usr/bin/python3
import RPi.GPIO as GPIO
from hx711 import HX711

# hx.set_reference_unit(1118673) #for 10kg load cell, tested with 8.708kg weight

try:
    hx711 = HX711(
        dout_pin=2,
        pd_sck_pin=3,
        channel='A',
        gain=64
    )

    hx711.reset()   # Before we start, reset the HX711 (optional)
    measures = hx711.get_raw_data(times=3)
finally:
    GPIO.cleanup()  # always do a GPIO cleanup in your scripts!

print(measures)
