from django.http import JsonResponse
import random

# from .device.spectral_sensor import SpectralSensor
# from .device.hanging_scale import HangingScale

# spectral_sensor = SpectralSensor()
# hanging_scale = HangingScale()

def get_hematuria(request):
    level = random.randint(0, 100) # re
    color = [1,2,3]

    return JsonResponse({'level': level, 'color': color})


def get_supply(request):
    # weight = scale.read_weight()
    # volume = weight / (1009)
    # volume = round(volume, 1)
    # percentage = int((volume/3)*100) # assuming 3 L bag

    volume = random.randint(0, 100) # re
    rate = random.randint(0, 100) # re
    percentage = random.randint(0, 100) # re
    time = random.randint(0, 100) # re

    return JsonResponse({'volume': volume, 'rate': rate, 'percent': percentage, 'time': time})
