'''
TIMER

Notes
- 

Documentation
- 

'''

import time


class Timer():
    def __init__(self, verbose=False):
        self.verbose = verbose
        
        self.start_time = None
        self.end_time = None

    def setup(self):
        print("Timer: setup")
        # self.start_time = 

    # convert between percent and duty_cycle
    def duty_cycle(self):
        pass

# example implementation
if __name__ == '__main__':
    timer = Timer()