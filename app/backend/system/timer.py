'''
TIMER

Notes
- Timer for notification system alerts

Documentation
- 

'''

import time


class Timer():
    def __init__(self, verbose=False):
        self.start_time = None
        self.verbose = verbose
    
    def start(self):
        if self.start_time == None:
            self.start_time = time.time()
            if self.verbose:
                print('timer started')
        else:
            if self.verbose:
                print('timer already started')

    def reset(self):
        self.start_time = None
        if self.verbose:
            print('timer reset')

    def duration(self, unit='min'):
        if self.start_time != None:
            duration = time.time() - self.start_time
            if unit == 'sec':
                return duration
            elif unit == 'min':
                return duration/60
            elif unit == 'hr':
                return duration/3600
            else:
                raise Exception(f"unit [{unit}] not valid")
        else:
            if self.verbose:
                print('timer not started')
            return None


# example implementation
if __name__ == '__main__':
    timer = Timer(verbose=True)

    print(timer.duration())
    timer.start()
    timer.start()
    time.sleep(2)
    print(timer.duration(unit='sec'))
    timer.reset()
    print(timer.duration())