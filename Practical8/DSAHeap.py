import numpy as np

from DSAHeapEntry import DSAHeapEntry


class DSAHeap:
    def __init__(self, capacity=100):
        if capacity < 1:
            raise ValueError("Capacity must be positive")
        self._heap = np.empty(capacity, dtype=object)
        self._count = 0

    def add(self, priority, value):
        if self._count == self._heap.size:
            raise ValueError("Heap is full")
        self._heap[self._count] = DSAHeapEntry(priority, value)
        self._count += 1
        self.trickleUp(self._count - 1)

    def remove(self):
        if self._count == 0:
            raise ValueError("Heap is empty")
        highest_entry = self._heap[0]
        self._count -= 1
        self._heap[0] = self._heap[self._count]
        self._heap[self._count] = None
        if self._count > 0:
            self.trickleDown(0)
        return highest_entry

    def display(self):
        if self._count == 0:
            print("Heap is empty")
        index = 0
        while index < self._count:
            entry = self._heap[index]
            print(index, ":", entry.getPriority(), entry.getValue())
            index += 1

    def trickleUp(self, index):
        moving = True
        while index > 0 and moving:
            parent_index = (index - 1) // 2
            if (self._heap[index].getPriority() >
                    self._heap[parent_index].getPriority()):
                temporary = self._heap[index]
                self._heap[index] = self._heap[parent_index]
                self._heap[parent_index] = temporary
                index = parent_index
            else:
                moving = False

    def trickleDown(self, index):
        self._trickleDownArray(self._heap, index, self._count)

    def _trickleDownArray(self, entries, index, heap_size):
        moving = True
        left_index = index * 2 + 1
        while left_index < heap_size and moving:
            larger_index = left_index
            right_index = left_index + 1
            if (right_index < heap_size and
                    entries[right_index].getPriority() >
                    entries[left_index].getPriority()):
                larger_index = right_index

            if (entries[larger_index].getPriority() >
                    entries[index].getPriority()):
                temporary = entries[index]
                entries[index] = entries[larger_index]
                entries[larger_index] = temporary
                index = larger_index
                left_index = index * 2 + 1
            else:
                moving = False

    def heapify(self, entries):
        parent_index = entries.size // 2 - 1
        while parent_index >= 0:
            self._trickleDownArray(entries, parent_index, entries.size)
            parent_index -= 1

    def heapSort(self, entries):
        self.heapify(entries)
        end_index = entries.size - 1
        while end_index > 0:
            temporary = entries[0]
            entries[0] = entries[end_index]
            entries[end_index] = temporary
            self._trickleDownArray(entries, 0, end_index)
            end_index -= 1
        return entries
