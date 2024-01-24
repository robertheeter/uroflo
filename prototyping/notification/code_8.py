# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Importing libraries 
import time
import board
import pwmio
import pygame

# Mellow sound for bag changes 
# playing sonar sound
pygame.init()
my_sound = pygame.mixer.Sound('sonar.mp3')
my_sound.play()
my_sound.set_volume(0.5) # can set sound volume from 0-1 
print('playing sonar sound')

# Defining pins on board GPIOs 
RED_PIN = board.D15  # Red LED pin
GREEN_PIN = board.D18  # Green LED pin
BLUE_PIN = board.D14  # Blue LED pin

FADE_SLEEP = 100  # Number of milliseconds to delay between changes.
# Increase to slow down, decrease to speed up.

# Define PWM outputs:
red = pwmio.PWMOut(RED_PIN)
green = pwmio.PWMOut(GREEN_PIN)
blue = pwmio.PWMOut(BLUE_PIN)


# Function to simplify setting duty cycle to percent value.

def duty_cycle(percent):
    return int(percent / 100.0 * 65535.0)

# while True:
#     # Fade from nothing up to full red.
#     for i in range(100):
#         red.duty_cycle = duty_cycle(i)
#         time.sleep(FADE_SLEEP / 1000)

#     # Now fade from violet (red + blue) down to red.
#     for i in range(100, -1, -1):
#         blue.duty_cycle = duty_cycle(i)
#         time.sleep(FADE_SLEEP / 1000)

#     # Fade from red to yellow (red + green).
#     for i in range(100):
#         green.duty_cycle = duty_cycle(i)
#         time.sleep(FADE_SLEEP / 1000)

#     # Fade from yellow to green.
#     for i in range(100, -1, -1):
#         red.duty_cycle = duty_cycle(i)
#         time.sleep(FADE_SLEEP / 1000)

#     # Fade from green to teal (blue + green).
#     for i in range(100):
#         blue.duty_cycle = duty_cycle(i)
#         time.sleep(FADE_SLEEP / 1000)

#     # Fade from teal to blue.
#     for i in range(100, -1, -1):
#         green.duty_cycle = duty_cycle(i)
#         time.sleep(FADE_SLEEP / 1000)

# make functions for setting to particular color or RGB value?

# Default color - uroflo blue
# while True: 
#     blue.duty_cycle = duty_cycle(4)
#     red.duty_cycle = duty_cycle(1)
#     green.duty_cycle = duty_cycle(2.74)
#     time.sleep(2)


# High emergency alert color: red 
# while True: 
#     red.duty_cycle = duty_cycle(5)
#     time.sleep(2)

# # Medium emergency alert color: orange 
while True: 
    blue.duty_cycle = duty_cycle(0.8)
    red.duty_cycle = duty_cycle(10)
    green.duty_cycle = duty_cycle(3.7)
    time.sleep(2)

# # Low emergency alert color: yellow 
# while True: 
#     blue.duty_cycle = duty_cycle(0)
#     red.duty_cycle = duty_cycle(10)
#     green.duty_cycle = duty_cycle(5)
#     time.sleep(2)




