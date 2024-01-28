# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Importing libraries 
import time
import board
import pwmio
import pygame

# Defining pins on board GPIOs 
RED_PIN = board.D8  # Red LED pin
GREEN_PIN = board.D7  # Green LED pin
BLUE_PIN = board.D1  # Blue LED pin

# Define PWM outputs:
red = pwmio.PWMOut(RED_PIN)
green = pwmio.PWMOut(GREEN_PIN)
blue = pwmio.PWMOut(BLUE_PIN)

# Function to simplify setting duty cycle to percent value.
def duty_cycle(percent):
    return int(percent / 100.0 * 65535.0)
    
# # default standard blue color
def default_LED():
    red.duty_cycle = duty_cycle(1)
    green.duty_cycle = duty_cycle(2.74)
    blue.duty_cycle = duty_cycle(4)

# red - high emergency
def red_LED():
    red.duty_cycle = duty_cycle(50)
    blue.duty_cycle = duty_cycle(0)
    green.duty_cycle = duty_cycle(0)

# orange - medium emergency
def orange_LED():
    red.duty_cycle = duty_cycle(50)
    blue.duty_cycle = duty_cycle(0)
    green.duty_cycle = duty_cycle(10)
    
# yellow - low emergency 
def yellow_LED():
    red.duty_cycle = duty_cycle(20)
    blue.duty_cycle = duty_cycle(0)
    green.duty_cycle = duty_cycle(10)

def mellow_alarm():
    pygame.init()
    my_sound = pygame.mixer.Sound('sonar.mp3') # only plays once
    my_sound.play()
    my_sound.set_volume(0.5) # can set sound volume from 0-1 

def harsh_alarm():
    my_sound = pygame.mixer.Sound('harsh.mp3') # repeats 4 times 
    my_sound.play()
    my_sound.set_volume(0.5) # can set sound volume from 0-1 

while True:
    FADE_SLEEP = 10
    default_LED()
    time.sleep(FADE_SLEEP / 10)
    yellow_LED()
    time.sleep(FADE_SLEEP / 10)
    orange_LED()
    time.sleep(FADE_SLEEP / 10)
    red_LED()
    time.sleep(FADE_SLEEP / 10)

    


# while True: 

#     default_LED()

#     # Condition A: saline bag volume
#     # assuming we will have inputted saline bag volume and current volume 

#     # calculate percentage saline volume remaining 
#     saline_percent = saline_current_volume / saline_bag_volume

#     if saline_percent <10: 
#         red_LED()
#         mellow_alarm()
#         # check if "Replace Saline Bag" button is pressed 
#             if replace_saline_bag_button is pressed: 
#                 default_LED()
                
        
#     if saline_percent >10 && <15: 
#         orange_LED()
#     if saline_percent >15 && <20 
#         yellow_LED()
    



FADE_SLEEP = 10  # Number of milliseconds to delay between changes.
# Increase to slow down, decrease to speed up.

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






