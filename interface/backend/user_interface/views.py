from django.http import JsonResponse
import random

# from .device.spectral_sensor import SpectralSensor
from .device.weight_sensor import WeightSensor

# spectral_sensor = SpectralSensor()
weight_sensor = WeightSensor(pd_sck_pin=19, dout_pin=26)

def get_hematuria(request):
    level = random.randint(0, 100) # re
    color = [1,2,3]

    return JsonResponse({'level': level, 'color': color})

def get_supply(request):
    volume = weight_sensor.volume()
    volume = volume / (1009)
    volume = round(volume, 1)
    percent = int((volume/3)*100) # assuming 3 L bag
    print(volume)
    print(percent)

    # volume = random.randint(0, 100) # re
    rate = random.randint(0, 100) # re
    percent = random.randint(0, 100) # re
    time = random.randint(0, 100) # re

    print(percent)
    
    return JsonResponse({'volume': volume, 'rate': rate, 'percent': percent, 'time': time})
