'''
HEMATURIA

Notes
- Measures blood concentration and hematuria severity using a spectral sensor

Documentation
- See components/spectral_sensor.py

'''

import time

from data import *

from components.spectral_sensor import SpectralSensor


# sensor/script parameters
SPECTRAL_SENSOR_REPLICATES = 20
DELAY = 1 # delay between iterations

# regression parameters
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

# severity level range parameters (blood concentration percent)
MAX_CLEAR = 1.0
MAX_MILD = 2.0
MAX_MODERATE = 4.0
MAX_SEVERE = 8.0

def hematuria():

    # instantiate spectral sensor
    spectral_sensor = SpectralSensor(led_pin=4, use_led=True, sensor_type='VIS', max=48000)

    # run continuously
    while True:

        # get intensities
        hematuria_intensities = spectral_sensor.read(replicates=SPECTRAL_SENSOR_REPLICATES)

        hematuria_violet = hematuria_intensities[450]
        hematuria_blue = hematuria_intensities[500]
        hematuria_green = hematuria_intensities[550]
        hematuria_yellow = hematuria_intensities[570]
        hematuria_orange = hematuria_intensities[600]
        hematuria_red = hematuria_intensities[650]

        # get predicted blood concentration from regression parameters and truncate
        hematuria_percent = w_violet*(1/(hematuria_violet - b_violet)) + w_blue*(1/(hematuria_blue - b_blue)) + w_green*(1/(hematuria_green - b_green)) + w_yellow*(1/(hematuria_yellow - b_yellow)) + w_orange*(1/(hematuria_orange - b_orange)) + w_red*(1/(hematuria_red - b_red))
        hematuria_percent = min(100, hematuria_percent) # set maximum hematuria percent to 100.0%
        hematuria_percent = max(0, hematuria_percent) # set minimum hematuria percent to 0.0%

        # get estimated hematuria severity level from blood concentration
        if hematuria_percent < MAX_CLEAR:
            hematuria_level = (24/MAX_CLEAR) * hematuria_percent
        elif hematuria_percent < MAX_MILD:
            hematuria_level = (((49-24)/(MAX_MILD-MAX_CLEAR)) * (hematuria_percent - MAX_CLEAR)) + 24
        elif hematuria_percent < MAX_MODERATE:
            hematuria_level = (((74-49)/(MAX_MILD-MAX_CLEAR)) * (hematuria_percent - MAX_CLEAR)) + 49
        elif hematuria_percent < MAX_SEVERE:
            hematuria_level = (((99-74)/(MAX_MILD-MAX_CLEAR)) * (hematuria_percent - MAX_CLEAR)) + 74
        else:
            hematuria_level = 99
        
        data = {
            'hematuria_percent': hematuria_percent,
            'hematuria_level': hematuria_level,
            'hematuria_violet': hematuria_violet,
            'hematuria_blue': hematuria_blue,
            'hematuria_green': hematuria_green,
            'hematuria_yellow': hematuria_yellow,
            'hematuria_orange': hematuria_orange,
            'hematuria_red': hematuria_red,
        }

        add_data(data=data, file='hematuria')
        
        time.sleep(DELAY)

if __name__ == '__main__':
    hematuria()
