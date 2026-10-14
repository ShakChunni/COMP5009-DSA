# Adapted from my COMP5008 Practical 6 stack.

from common.DSALinkedList import DSALinkedList


class DSAStack:
    def __init__(self):
        self._list = DSALinkedList()

    def isEmpty(self):
        return self._list.isEmpty()

    def push(self, value):
        self._list.insertFirst(value)

    def pop(self):
        return self._list.removeFirst()

    def top(self):
        return self._list.peekFirst()
