'''
LIGHT & SOUND

About
- LED strip light using 3 R, G, and B N-channel MOSFETs
- Speaker with sound alerts

For
- Notification system

Notes
- Pin allocation:
  PIN 24 (GPIO 8), PIN 26 (GPIO 7), PIN 28 (GPIO 1), PIN 30 (Ground)

Documentation
- Guide: https://learn.adafruit.com/rgb-led-strips

'''

import time
import board
import pwmio
import pygame


class LightSound():
    def __init__(self, red_pin, green_pin, blue_pin, verbose=False):
        self.red_pin = red_pin # GPIO red pin (BCM)
        self.green_pin = green_pin # GPIO green pin (BCM)
        self.blue_pin = blue_pin # GPIO blue pin (BCM)

        self.verbose = verbose

        self.setup()

    def setup(self):
        print("LightSound: setup")
        self.red = pwmio.PWMOut(self.red_pin)
        self.green = pwmio.PWMOut(self.green_pin)
        self.blue = pwmio.PWMOut(self.blue_pin)

    # convert between percent and duty_cycle
    def duty_cycle(self, percent):
        return int(percent / 100.0 * 65535.0)

    # turn on LED to color
    def light(self, color):
        if color not in ['off', 'default', 'yellow', 'orange', 'red']:
            raise Exception(f"LightSound: color = {color} not available")
        
        if self.verbose:
            print(f"LightSound: light (color = {color})")
        
        if color == 'off':
            self.red.duty_cycle = self.duty_cycle(0)
            self.green.duty_cycle = self.duty_cycle(0)
            self.blue.duty_cycle = self.duty_cycle(0)
        
        elif color == 'default':
            self.red.duty_cycle = self.duty_cycle(1)
            self.green.duty_cycle = self.duty_cycle(2.74)
            self.blue.duty_cycle = self.duty_cycle(4)
            
        elif color == 'yellow':
            self.red.duty_cycle = self.duty_cycle(20)
            self.blue.duty_cycle = self.duty_cycle(0)
            self.green.duty_cycle = self.duty_cycle(10)

        elif color == 'orange':
            self.red.duty_cycle = self.duty_cycle(50)
            self.blue.duty_cycle = self.duty_cycle(0)
            self.green.duty_cycle = self.duty_cycle(10)

        elif color == 'red':
            self.red.duty_cycle = self.duty_cycle(50)
            self.blue.duty_cycle = self.duty_cycle(0)
            self.green.duty_cycle = self.duty_cycle(0)

    # play audio from speaker
    def sound(self, tone):
        if tone not in ['chime', 'alarm']:
            raise Exception(f"LightSound: tone = {tone} not available")
        
        if self.verbose:
            print(f"LightSound: sound (tone = {tone})")

        pygame.init()

        if tone == 'chime':
            audio = pygame.mixer.Sound('sound/chime.mp3') # play 1 time

        elif tone == 'alarm':
            audio = pygame.mixer.Sound('sound/alarm.mp3') # play 4 times
        
        audio.set_volume(1.0)
        audio.play()

    def shutdown(self):
        print("LightSound: shutdown")
        self.light('off')
        self.red.deinit()
        self.green.deinit()
        self.blue.deinit()
        pygame.quit()


# example implementation
if __name__ == '__main__':
    light_sound = LightSound(red_pin=board.D8, green_pin=board.D7, blue_pin=board.D1, verbose=True) # use BOARD.D[GPIO] numbering (NOT pin numbering)
    time.sleep(2) # wait for setup

    for color in ['default', 'off', 'yellow', 'orange', 'red']:
        light_sound.light(color=color)
        time.sleep(4)
    
    for tone in ['chime', 'alarm']:
        light_sound.sound(tone=tone)
        # for i in range(2000):
        #     print(i)
        # time.sleep(16)

    # light_sound.shutdown()
