from pump_class import Pump

if __name__ == '__main__':
    # initialize pump
    pump = Pump(step_pin=21, dir_pin=20, en_pin=16)

    # accelerate pump to 100 mL/min and run for 15 seconds
    pump.accelerate(100)
    pump.run(15)

    # decelerate pump to 50 mL/min and run for 10 seconds
    pump.accelerate(50)
    pump.run(10)

    # stop motor
    pump.stop()

