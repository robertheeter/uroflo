'''
BUTTON

Notes
- For user interface

- Momentary push button

- Pin allocation:
  PIN 17 (3.3 V) [RED], PIN 19 (GPIO 10) [BLUE], PIN 25 (Ground) [BLACK]

Documentation
- Wiring: https://hackster.imgix.net/uploads/attachments/1648376/button_diagram_z7KQmf80jt.png?auto=compress%2Cformat&w=1280&h=960&fit=max

'''

import RPi.GPIO as GPIO
import time
import os


class Button():
    def __init__(self, pin, orientation=0, verbose=False):
        self.pin = pin # GPIO input pin (BCM)

        self.verbose = verbose # toggles printing of information to terminal

        self.setup()

    def setup(self):
        print("Button: setup")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) # BCM mode

        GPIO.setup(self.pin, GPIO.IN)

    def pressed(self):
        if GPIO.input(self.pin) == GPIO.HIGH:
            if self.verbose:
                print("Button: pressed = True")
            return True
        else:
            if self.verbose:
                print("Button: pressed = False")
            return False

    def shutdown(self):
        print(f"Button: shutdown")
        GPIO.cleanup()


# example implementation
if __name__ == '__main__':
    os.chdir('..') # change current directory

    button = Button(pin=10, verbose=True) # use GPIO numbering (BCM) (NOT pin numbering)
    time.sleep(2) # wait for setup

    for _ in range(40):
        button.pressed()
        time.sleep(0.5)

    button.shutdown()
    