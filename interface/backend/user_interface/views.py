from django.http import JsonResponse

from .device.spectral_sensor import SpectralSensor
from .device.hanging_scale import HangingScale

spectral_sensor = SpectralSensor()
hanging_scale = HangingScale()

def get_hematuria(request):

    # replace value with the code needed to read the hematuria sensor
    # and get the percentage

    value = random.randint(0, 100) # re
    # value = 1242

    return JsonResponse({'raw': value})


def get_bag(request):

    # weight = scale.read_weight()
    # volume = weight / (1009)
    # volume = round(volume, 1)
    # percentage = int((volume/3)*100) # assuming 3 L bag
    volume = random.randint(0, 100) # re
    percentage = random.randint(0, 100) # re
    flow = 0
    return JsonResponse({'volume': volume, 'percent_volume': percentage, 'flow': flow})
