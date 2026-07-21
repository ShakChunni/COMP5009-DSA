import numpy as np
def find_min_max_temp(temps):

    max_temp = temps[0]
    min_temp = temps[0]

    for i in temps:
        if i > max_temp:
            max_temp = i
        elif i < min_temp:
            min_temp = i

    print(f"Max Temperature: {max_temp}°C, Min Temperature: {min_temp}°C")
