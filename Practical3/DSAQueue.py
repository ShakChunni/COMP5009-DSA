#
# Data Structures and Algorithms
# Practical 3: Stacks and Queues
# DSAQueue, DSAShufflingQueue, and DSACircularQueue Implementations
#

import numpy as np


class DSAQueue:
    """
    Abstract base class for queues.
    Subclasses must implement peek(), enqueue(value), and dequeue().
    """
    DEFAULT_CAPACITY = 100

    def __init__(self, maxCapacity=DEFAULT_CAPACITY):
        if type(maxCapacity) is not int:
            raise TypeError("maxCapacity must be an integer")
        if maxCapacity <= 0:
            raise ValueError("maxCapacity must be greater than zero")

        self._queue = np.empty(maxCapacity, dtype=object)
        self._count = 0

    # -------------------------------------------------------------------------
    # Accessor methods
    # -------------------------------------------------------------------------
    def getCount(self):
        return self._count

    def isEmpty(self):
        return self._count == 0

    def isFull(self):
        return self._count == len(self._queue)

    def peek(self):
        raise NotImplementedError("Subclass must implement peek()")

    # -------------------------------------------------------------------------
    # Mutator methods
    # -------------------------------------------------------------------------
    def enqueue(self, value):
        raise NotImplementedError("Subclass must implement enqueue()")

    def dequeue(self):
        raise NotImplementedError("Subclass must implement dequeue()")

    def __len__(self):
        return self._count


class DSAShufflingQueue(DSAQueue):
    """
    FIFO Queue implemented by shifting/shuffling elements forward upon dequeue.
    Time Complexity:
      enqueue: O(1)
      dequeue: O(N) (shifting N elements left)
      peek: O(1)
    """

    def __init__(self, maxCapacity=DSAQueue.DEFAULT_CAPACITY):
        super().__init__(maxCapacity)

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
        front_val = self.peek()
        # By-hand manual element shuffling
        for i in range(0, self._count - 1):
            self._queue[i] = self._queue[i + 1]
        self._count -= 1
        self._queue[self._count] = None
        return front_val

    def display(self):
        print("DSAShufflingQueue (front -> rear): [", end="")
        for i in range(self._count):
            if i > 0:
                print(", ", end="")
            print(repr(self._queue[i]), end="")
        print("]")

    def __str__(self):
        items = []
        for i in range(self._count):
            items.append(str(self._queue[i]))
        return "[" + ", ".join(items) + "]"


class DSACircularQueue(DSAQueue):
    """
    FIFO Queue implemented using circular wrap-around buffer.
    Time Complexity:
      enqueue: O(1)
      dequeue: O(1)
      peek: O(1)
    """

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
        self._rear = (self._rear + 1) % len(self._queue)
        self._count += 1

    def dequeue(self):
        front_val = self.peek()
        self._queue[self._front] = None
        self._front = (self._front + 1) % len(self._queue)
        self._count -= 1
        return front_val

    def display(self):
        print("DSACircularQueue (front -> rear): [", end="")
        current = self._front
        for i in range(self._count):
            if i > 0:
                print(", ", end="")
            print(repr(self._queue[current]), end="")
            current = (current + 1) % len(self._queue)
        print("]")

    def __str__(self):
        items = []
        current = self._front
        for _ in range(self._count):
            items.append(str(self._queue[current]))
            current = (current + 1) % len(self._queue)
        return "[" + ", ".join(items) + "]"


# Polymorphic aliases matching lecture and practical sheets
ShufflingQueue = DSAShufflingQueue
CircularQueue = DSACircularQueue


if __name__ == "__main__":
    print("=== Testing DSAShufflingQueue ===")
    sq = DSAShufflingQueue(5)
    sq.enqueue(1)
    sq.enqueue(2)
    sq.enqueue(3)
    sq.display()
    print("dequeue():", sq.dequeue())
    sq.display()

    print("\n=== Testing DSACircularQueue ===")
    cq = DSACircularQueue(3)
    cq.enqueue("A")
    cq.enqueue("B")
    cq.enqueue("C")
    cq.display()
    print("dequeue():", cq.dequeue())
    print("enqueue('D') wrapping around:")
    cq.enqueue("D")
    cq.display()
    print("dequeue():", cq.dequeue())
    print("dequeue():", cq.dequeue())
    print("dequeue():", cq.dequeue())
    print("isEmpty():", cq.isEmpty())
