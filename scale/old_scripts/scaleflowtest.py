from statistics import mean
import random
import time

class Weight:
    def __init__(self, weight=500):
        self.weight = weight
        self.time = time.time()

    def get_weight(self):
        current_time = time.time()
        delta_time = current_time - self.time
        rate = 0.5 # decrease weight by rate every 1 second
        noise = random.uniform(0, 2)
        change = delta_time*rate + noise # add noise to simulate real world
        weight = self.weight - change
        return weight




weight = Weight()

data = []
window = 500

start_time = time.time()
start_weight = -1

while True:

    reading = weight.get_weight()
    data.append(reading)

    if len(data) < window:
        continue

    avg_weight = mean(data)

    if start_weight == -1:
        start_weight = avg_weight

    data.pop(0)

    if time.time() - start_time >= 1:
        flow_rate = (start_weight - avg_weight)*60
        print(f'Flow rate: {flow_rate}')
        print(f'Weight: {avg_weight}\n')

        start_time = time.time()
        start_weight = avg_weight
    
    time.sleep(0.1)