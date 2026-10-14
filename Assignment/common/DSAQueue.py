# Adapted from my COMP5008 Practical 6 queue.
from common.DSALinkedList import DSALinkedList


class DSAQueue:
    def __init__(self):
        self._list = DSALinkedList()

    def isEmpty(self):
        return self._list.isEmpty()

    def enqueue(self, value):
        self._list.insertLast(value)

    def dequeue(self):
        return self._list.removeFirst()
