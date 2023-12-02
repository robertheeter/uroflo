import time
from scale_class import Scale


if __name__ == '__main__':
    scale = Scale(pd_sck_pin=2, dout_pin=3)
    
    while True:
        try:
            weight = scale.read_weight()
            volume = weight / (1009/1000)
            print(f'Volume: {volume} mL')

            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scale.stop()
