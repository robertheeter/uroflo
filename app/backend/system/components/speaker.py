'''
SPEAKER

Notes
- For notification system

- USB speaker with sound alerts

- Pin allocation:
  USB

Documentation
- Guide: https://projects.raspberrypi.org/en/projects/generic-python-playing-sound-files

'''

import time
import pygame
import os


class Speaker():
    def __init__(self, verbose=False):
        self.verbose = verbose

        self.setup()

    def setup(self):
        print("Speaker: setup")
        pygame.init()

    # play audio from speaker
    def play(self, file, volume=1.0):
        if not os.path.exists(file):
            raise Exception(f"Speaker: file = {file} not found")
        
        if self.verbose:
            print(f"Speaker: play (file = {file})")
        
        audio = pygame.mixer.Sound(file)
        audio.set_volume(volume)
        audio.play()

    # stop audio from speaker
    def stop(self):
        pygame.quit()

    def shutdown(self):
        print("Speaker: shutdown")
        self.stop()


# example implementation
if __name__ == '__main__':
    os.chdir('..') # change current directory
    
    speaker = Speaker(verbose=True)
    time.sleep(2) # wait for setup

    for file in ['sound/echo.mp3', 'sound/alarm.mp3']:
        speaker.play(file=file, volume=1.0)
        time.sleep(10)

    speaker.shutdown()
