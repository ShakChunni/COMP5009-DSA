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


if __name__ == "__main__":
    print("=== Testing DSAQueue (LinkedList-backed) ===")
    queue = DSAQueue()
    print("Initial isEmpty():", queue.isEmpty())

    queue.enqueue("Task 1")
    queue.enqueue("Task 2")
    queue.enqueue("Task 3")
    print("Queue:", queue)
    print("peek():", queue.peek())
    print("dequeue():", queue.dequeue())
    print("Queue after dequeue:", queue)
