class DSAListNode:
    def __init__(self, inValue):
        self.value = inValue
        self.next = None
        self.prev = None

    def getValue(self):
        return self.value

    def setValue(self, inValue):
        self.value = inValue

    def getNext(self):
        return self.next

    def setNext(self, newNext):
        self.next = newNext

    def getPrev(self):
        return self.prev

    def setPrev(self, newPrev):
        self.prev = newPrev


class DSALinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        return self.head is None

    def insertFirst(self, newValue):
        newNd = DSAListNode(newValue)
        if self.isEmpty():
            self.head = newNd
            self.tail = newNd
        else:
            newNd.setNext(self.head)
            self.head.setPrev(newNd)
            self.head = newNd

    def insertLast(self, newValue):
        newNd = DSAListNode(newValue)
        if self.isEmpty():
            self.head = newNd
            self.tail = newNd
        else:
            newNd.setPrev(self.tail)
            self.tail.setNext(newNd)
            self.tail = newNd

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

        nodeValue = self.head.getValue()
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.getNext()
            self.head.setPrev(None)

        return nodeValue

    def removeLast(self):
        if self.isEmpty():
            raise IndexError("List is empty")

        nodeValue = self.tail.getValue()
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.getPrev()
            self.tail.setNext(None)

        return nodeValue

    def __str__(self):
        result = "["
        currNd = self.head
        first = True
        while currNd is not None:
            if not first:
                result += ", "
            result += str(currNd.getValue())
            first = False
            currNd = currNd.getNext()
        return result + "]"
