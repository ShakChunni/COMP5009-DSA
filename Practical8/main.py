import numpy as np

from DSAHeap import DSAHeap
from DSAHeapEntry import DSAHeapEntry


def loadEntries(filename):
    count = 0
    with open(filename, "r") as input_file:
        for line in input_file:
            count += 1

    entries = np.empty(count, dtype=object)
    index = 0
    with open(filename, "r") as input_file:
        for line in input_file:
            comma_index = 0
            while comma_index < len(line) and line[comma_index] != ",":
                comma_index += 1
            if comma_index == len(line):
                raise ValueError("CSV line must contain a comma")
            end_index = len(line)
            while (end_index > comma_index and
                   (line[end_index - 1] == "\n" or
                    line[end_index - 1] == "\r")):
                end_index -= 1
            priority = int(line[:comma_index])
            value = line[comma_index + 1:end_index]
            entries[index] = DSAHeapEntry(priority, value)
            index += 1
    return entries


def main():
    heap = DSAHeap(100)
    sorted_entries = None
    choice = ""

    while choice != "0":
        print("\n1. Add entry")
        print("2. Remove highest priority entry")
        print("3. Display heap")
        print("4. Load CSV and apply HeapSort")
        print("5. Display sorted CSV entries")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            priority = int(input("Enter priority: "))
            value = input("Enter value: ")
            heap.add(priority, value)
        elif choice == "2":
            entry = heap.remove()
            print("Removed:", entry.getPriority(), entry.getValue())
        elif choice == "3":
            heap.display()
        elif choice == "4":
            sorted_entries = loadEntries("RandomNames7000.csv")
            heap.heapSort(sorted_entries)
            print("Sorted records:", sorted_entries.size)
            if sorted_entries.size > 0:
                print("Smallest priority:", sorted_entries[0].getPriority())
                print("Largest priority:",
                      sorted_entries[sorted_entries.size - 1].getPriority())
        elif choice == "5":
            if sorted_entries is None:
                print("Load and sort the CSV first")
            else:
                index = 0
                while index < sorted_entries.size:
                    entry = sorted_entries[index]
                    print(entry.getPriority(), entry.getValue())
                    index += 1
        elif choice != "0":
            print("Invalid option")


if __name__ == "__main__":
    main()
