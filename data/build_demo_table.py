import random
import math

def make_values(avg, width, n):
    return [random.uniform(-width+avg, width+avg)  for _ in range(n)]

quantity_1 = [math.sin(hour * math.pi / 12) * 50 for hour in range(0, 24)]
quantity_2 = [math.sin(hour * math.pi / 12) * 50 for hour in range(0, 24)]



N = 3
W = 10
with open("demo.csv", 'w') as f:
    f.write(f'hour, value1, value2\n')
    hour = 0
    for desired_avg1, desired_avg2 in zip(quantity_1, quantity_2):
        r1 = make_values(desired_avg1, W, N)
        r2 = make_values(desired_avg2, W*100, N)
        for v1, v2 in zip(r1, r2):
            f.write(f'{hour}, {v1}, {v2}\n')
        hour += 1
