#
# Data Structures and Algorithms
# Practical 3: Stacks and Queues
# DSAStack Implementation
#

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

    # -------------------------------------------------------------------------
    # Accessor methods
    # -------------------------------------------------------------------------
    def getCount(self):
        return self._count

    def isEmpty(self):
        return self._count == 0

    def isFull(self):
        return self._count == len(self._stack)

    def top(self):
        if self.isEmpty():
            raise IndexError("Stack is empty")
        return self._stack[self._count - 1]

    def peek(self):
        """Synonym for top()."""
        return self.top()

    # -------------------------------------------------------------------------
    # Mutator methods
    # -------------------------------------------------------------------------
    def push(self, value):
        if self.isFull():
            raise IndexError("Stack is full")
        self._stack[self._count] = value
        self._count += 1

    def pop(self):
        top_val = self.top()
        self._count -= 1
        self._stack[self._count] = None
        return top_val

    # -------------------------------------------------------------------------
    # Support / display methods
    # -------------------------------------------------------------------------
    def display(self):
        print("Stack (top -> bottom): [", end="")
        for i in range(self._count - 1, -1, -1):
            if i < self._count - 1:
                print(", ", end="")
            print(repr(self._stack[i]), end="")
        print("]")

    def __len__(self):
        return self._count

    def __str__(self):
        items = []
        for i in range(self._count - 1, -1, -1):
            items.append(str(self._stack[i]))
        return "[" + ", ".join(items) + "]"


if __name__ == "__main__":
    print("=== Testing DSAStack ===")
    stack = DSAStack(5)
    print("Initial isEmpty():", stack.isEmpty())
    print("Pushing: 10, 20, 30")
    stack.push(10)
    stack.push(20)
    stack.push(30)
    stack.display()
    print("top():", stack.top())
    print("pop():", stack.pop())
    print("After pop:")
    stack.display()
    print("count:", stack.getCount())
