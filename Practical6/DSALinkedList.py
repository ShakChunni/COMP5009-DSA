class DSAListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getNext(self):
        return self.next

    def setNext(self, new_next):
        self.next = new_next

    def getPrev(self):
        return self.prev

    def setPrev(self, new_prev):
        self.prev = new_prev


class DSALinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        return self.head is None

    def insertFirst(self, new_value):
        new_node = DSAListNode(new_value)
        if self.isEmpty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.setNext(self.head)
            self.head.setPrev(new_node)
            self.head = new_node

    def insertLast(self, new_value):
        new_node = DSAListNode(new_value)
        if self.isEmpty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.setPrev(self.tail)
            self.tail.setNext(new_node)
            self.tail = new_node

    def peekFirst(self):
        if self.isEmpty():
            raise IndexError("List is empty")
        return self.head.getValue()

    def peekLast(self):
        if self.isEmpty():
            raise IndexError("List is empty")
        return self.tail.getValue()

    def removeFirst(self):
        if self.isEmpty():
            raise IndexError("List is empty")

        node_value = self.head.getValue()
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.getNext()
            self.head.setPrev(None)

        return node_value

    def removeLast(self):
        if self.isEmpty():
            raise IndexError("List is empty")

        node_value = self.tail.getValue()
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.getPrev()
            self.tail.setNext(None)

        return node_value

    def delete(self, target_value):
        if self.isEmpty():
            raise KeyError("List is empty")

        current_node = self.head
        found = False
        while current_node is not None and not found:
            if current_node.getValue() == target_value:
                found = True
            else:
                current_node = current_node.getNext()

        if not found:
            raise KeyError("Value not found in list: " + str(target_value))

        if current_node == self.head and current_node == self.tail:
            self.head = None
            self.tail = None
        elif current_node == self.head:
            self.head = self.head.getNext()
            self.head.setPrev(None)
        elif current_node == self.tail:
            self.tail = self.tail.getPrev()
            self.tail.setNext(None)
        else:
            previous_node = current_node.getPrev()
            next_node = current_node.getNext()
            previous_node.setNext(next_node)
            next_node.setPrev(previous_node)

    def has(self, target_value):
        current_node = self.head
        found = False
        while current_node is not None and not found:
            if current_node.getValue() == target_value:
                found = True
            else:
                current_node = current_node.getNext()
        return found

    def count(self):
        total = 0
        current_node = self.head
        while current_node is not None:
            total += 1
            current_node = current_node.getNext()
        return total

    def __iter__(self):
        current_node = self.head
        while current_node is not None:
            yield current_node.getValue()
            current_node = current_node.getNext()

    def __str__(self):
        result = "["
        current_node = self.head
        is_first = True
        while current_node is not None:
            if not is_first:
                result += ", "
            result += str(current_node.getValue())
            is_first = False
            current_node = current_node.getNext()
        return result + "]"
