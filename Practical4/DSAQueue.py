from DSALinkedList import DSALinkedList


class DSAQueue:
    def __init__(self):
        self._list = DSALinkedList()

    def isEmpty(self):
        return self._list.isEmpty()

    def enqueue(self, value):
        self._list.insertLast(value)

    def dequeue(self):
        return self._list.removeFirst()

    def peek(self):
        return self._list.peekFirst()

    def __str__(self):
        return str(self._list)
