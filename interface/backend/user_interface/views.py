from django.http import JsonResponse
import random

from .device.spectral_sensor import SpectralSensor
from .device.weight_sensor import WeightSensor

spectral_sensor = SpectralSensor(led_pin=4, sensor_type='VIS', max=48000, verbose=False)
weight_sensor = WeightSensor(pd_sck_pin=14, dout_pin=15, verbose=True)

def get_hematuria(request):
    # sensor_type = 'VIS'

    level = random.randint(0, 100)
    color = [1,2,3]

    return JsonResponse({'level': int(level),
                         'color': color})

def get_supply(request):
    volume = weight_sensor.mass() / 1009 # convert mg to L with density
    percent = int(min((volume/3)*100, 100)) # using 3 L bag

    rate = random.randint(0, 100) # random integer for noww
    time = random.randint(0, 100) # random integer for now

    return JsonResponse({'volume': format(volume, '1.1f'),
                         'rate': format(rate, '.1f'),
                         'percent': int(percent),
                         'time': int(time)})
