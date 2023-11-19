'''
TOUCH INTERFACE

About
- 10.1" LCD touchscreen (1024x600 pixels, USB capacitive touch)

Notes
- 

Documentation
- Amazon: https://www.amazon.com/Hosyond-Capacitive-Portable-1024X600-Raspberry/dp/B0BHQRSDZR



development notes

- https://docs.djangoproject.com/en/4.2/contents/
    - left off at part 7, customize the admin form
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!


- to continually update website: use Django channels or AJAX
    - https://channels.readthedocs.io/en/stable/
    - Django channels might be best


- https://docs.djangoproject.com/en/4.2/intro/tutorial01/
- https://pimylifeup.com/raspberry-pi-django/



'''

# import time
# import RPi.GPIO as GPIO

# # touch interface class
# class TouchInterface():
#     def __init__(self, verbose=False):
#         self.in1 = pins[0] # GPIO input pin 1

#         self.verbose = verbose # toggles printing of information to terminal
#         self.setup()

#     def setup(self):
#         if self.verbose:
#             print(f"LinearActuator: pin in1 = {self.in1}")
#             print(f"LinearActuator: pin in2 = {self.in2}")
#             print(f"LinearActuator: pin en = {self.en}")
#             print(f"LinearActuator: freq = {self.freq}")

#         GPIO.setmode(GPIO.BCM) # set up GPIO pins
    
#     def run(self, dir='forward', speed=100, dur=-1):
        

#     def stop(self):
#         print(f"LinearActuator: stop")
        

#     def off(self):
#         print(f"LinearActuator: off")
        

# # testing
# if __name__ == '__main__':
#     ta = TouchInterface(verbose=True)

#     ta.run('backward', 100, 6)
#     time.sleep(1) # wait
#     la.stop()
#     la.off()
