import numpy as np

from activity1 import find_min_max_temp
from activity2 import read_process_temps


def main():
    #activity 1:
    temps = np.array([-22, 30, 252, 28, 33, 31, 27])
    find_min_max_temp(temps)

    #activity 2:
    read_process_temps("temperatures_365_days.csv")


if __name__ == "__main__":
    main()
