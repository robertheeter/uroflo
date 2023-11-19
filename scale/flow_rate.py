import time
from scale_class import Scale


if __name__ == '__main__':
    scale = Scale(pd_sck_pin=2, dout_pin=3)

    while True:
        try:
            # calculate flow rate every 60 seconds
            flow_rate = scale.calculate_flow_rate(60)
            print(f'Flow rate: {flow_rate} mL/min')
        except (KeyboardInterrupt, SystemExit):
            scale.stop()