import numpy as np


class DSAQueue:
    DEFAULT_CAPACITY = 100

    def __init__(self, maxCapacity=DEFAULT_CAPACITY):
        if type(maxCapacity) is not int:
            raise TypeError("maxCapacity must be an integer")
        if maxCapacity <= 0:
            raise ValueError("maxCapacity must be greater than zero")

        self._queue = np.empty(maxCapacity, dtype=object)
        self._count = 0

    def getCount(self):
        return self._count

    def isEmpty(self):
        return self._count == 0

    def isFull(self):
        return self._count == self._queue.size

    def peek(self):
        raise NotImplementedError("Subclass must implement peek()")

    def enqueue(self, value):
        raise NotImplementedError("Subclass must implement enqueue()")

    def dequeue(self):
        raise NotImplementedError("Subclass must implement dequeue()")


class DSAShufflingQueue(DSAQueue):
    def peek(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self._queue[0]

    def enqueue(self, value):
        if self.isFull():
            raise IndexError("Queue is full")
        self._queue[self._count] = value
        self._count += 1

    def dequeue(self):
        value = self.peek()
        index = 0
        while index < self._count - 1:
            self._queue[index] = self._queue[index + 1]
            index += 1
        self._count -= 1
        self._queue[self._count] = None
        return value

    def __str__(self):
        result = "["
        index = 0
        while index < self._count:
            if index > 0:
                result += ", "
            result += str(self._queue[index])
            index += 1
        return result + "]"


class DSACircularQueue(DSAQueue):
    def __init__(self, maxCapacity=DSAQueue.DEFAULT_CAPACITY):
        super().__init__(maxCapacity)
        self._front = 0
        self._rear = 0

    def peek(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self._queue[self._front]

    def enqueue(self, value):
        if self.isFull():
            raise IndexError("Queue is full")
        self._queue[self._rear] = value
        self._rear = (self._rear + 1) % self._queue.size
        self._count += 1

    def dequeue(self):
        value = self.peek()
        self._queue[self._front] = None
        self._front = (self._front + 1) % self._queue.size
        self._count -= 1
        return value

    def __str__(self):
        result = "["
        index = 0
        position = self._front
        while index < self._count:
            if index > 0:
                result += ", "
            result += str(self._queue[position])
            position = (position + 1) % self._queue.size
            index += 1
        return result + "]"
