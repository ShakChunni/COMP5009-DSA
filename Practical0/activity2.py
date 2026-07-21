import numpy as np


def read_process_temps(file_path):
    dates = np.empty(365, dtype='object')
    temps = np.zeros(365, dtype='float')

    with open(file_path, 'r', encoding='latin-1') as file:
        header = file.readline()
        array_index = 0
        for line in file:
            current_date = ""
            current_temp = ""
            found_comma = False

            for char in line:
                if char == ',':
                    found_comma = True
                elif not found_comma:
                    current_date += char
                else:
                   
                    current_temp += char
            
            dates[array_index] = current_date
            temps[array_index] = float(current_temp)
            array_index += 1


        max_temp = temps[0]
        min_temp = temps[0]
        max_day = dates[0]
        min_day = dates[0]
        for i in range(array_index):
            if temps[i] > max_temp:
                max_temp = temps[i]
                max_day = dates[i]
            elif temps[i] < min_temp:
                min_temp = temps[i]
                min_day = dates[i]
    print("Hottest day:", max_day, "with temperature", max_temp, "°C")
    print("Coldest day:", min_day, "with temperature", min_temp, "°C")

       
