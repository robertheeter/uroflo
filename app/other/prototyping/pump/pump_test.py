from pump_class import Pump

if __name__ == '__main__':
    # initialize pump
    pump = Pump(step_pin=21, dir_pin=20, en_pin=16)
    time = 800 # time program will run for
    # accelerate pump to 100 mL/min and run for 15 seconds
    pump.accelerate(100)
    pump.run(time)

    # decelerate pump to 50 mL/min and run for 10 seconds
    # pump.accelerate(50)
    # pump.run(10)
    if (KeyboardInterrupt, SystemExit):
        pump.stop()
    # stop motor
    pump.stop()

