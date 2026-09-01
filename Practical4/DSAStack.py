from DSALinkedList import DSALinkedList


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

    def peek(self):
        return self.top()

    def __str__(self):
        return str(self._list)
