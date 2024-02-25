import time
from .scale_class import Scale


if __name__ == '__main__':
    scale = Scale(pd_sck_pin=18, dout_pin=23)
    
    while True:
        try:
            time.sleep(5)
            weight = scale.read_weight()
            volume = weight / (1009/1000)
            print(f'Volume: {volume} mL')

            
        except (KeyboardInterrupt, SystemExit):
            scale.stop()
