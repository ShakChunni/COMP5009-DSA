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


if __name__ == "__main__":
    print("=== Testing DSAStack (LinkedList-backed) ===")
    stack = DSAStack()
    print("Initial isEmpty():", stack.isEmpty())

    stack.push(10)
    stack.push(20)
    stack.push(30)
    print("Stack:", stack)
    print("top():", stack.top())
    print("pop():", stack.pop())
    print("Stack after pop:", stack)
