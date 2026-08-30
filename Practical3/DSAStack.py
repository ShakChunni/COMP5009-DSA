import numpy as np


class DSAStack:
    DEFAULT_CAPACITY = 100

    def __init__(self, maxCapacity=DEFAULT_CAPACITY):
        if type(maxCapacity) is not int:
            raise TypeError("maxCapacity must be an integer")
        if maxCapacity <= 0:
            raise ValueError("maxCapacity must be greater than zero")

        self._stack = np.empty(maxCapacity, dtype=object)
        self._count = 0

    def getCount(self):
        return self._count

    def isEmpty(self):
        return self._count == 0

    def isFull(self):
        return self._count == self._stack.size

    def top(self):
        if self.isEmpty():
            raise IndexError("Stack is empty")
        return self._stack[self._count - 1]

    def push(self, value):
        if self.isFull():
            raise IndexError("Stack is full")
        self._stack[self._count] = value
        self._count += 1

    def pop(self):
        value = self.top()
        self._count -= 1
        self._stack[self._count] = None
        return value
