from DSALinkedList import DSALinkedList, DSAListNode


class DSAGraphNode:
    def __init__(self, label, value=None):
        if label is None:
            raise ValueError("Label cannot be None")
        self._label = str(label)
        self._value = value
        self._adjacent = DSALinkedList()
        self._visited = False

    def getLabel(self):
        return self._label

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def getAdjacent(self):
        return self._adjacent

    def setVisited(self):
        self._visited = True

    def clearVisited(self):
        self._visited = False

    def getVisited(self):
        return self._visited

    def isVisited(self):
        return self._visited

    def addEdge(self, destination_node):
        current_node = self._adjacent.head
        duplicate_found = False
        while current_node is not None and not duplicate_found:
            if current_node.getValue().getLabel() == destination_node.getLabel():
                duplicate_found = True
            else:
                current_node = current_node.getNext()

        if not duplicate_found:
            if self._adjacent.isEmpty():
                self._adjacent.insertLast(destination_node)
            elif destination_node.getLabel() < self._adjacent.head.getValue().getLabel():
                self._adjacent.insertFirst(destination_node)
            elif destination_node.getLabel() > self._adjacent.tail.getValue().getLabel():
                self._adjacent.insertLast(destination_node)
            else:
                scan_node = self._adjacent.head
                inserted = False
                while scan_node is not None and not inserted:
                    if destination_node.getLabel() < scan_node.getValue().getLabel():
                        new_node = DSAListNode(destination_node)
                        previous_node = scan_node.getPrev()
                        previous_node.setNext(new_node)
                        new_node.setPrev(previous_node)
                        new_node.setNext(scan_node)
                        scan_node.setPrev(new_node)
                        inserted = True
                    else:
                        scan_node = scan_node.getNext()

    def deleteEdge(self, destination_node):
        self._adjacent.delete(destination_node)

    def hasEdge(self, destination_node):
        return self._adjacent.has(destination_node)

    def getUnvisitedAdjacent(self):
        current_node = self._adjacent.head
        unvisited_node = None
        while current_node is not None and unvisited_node is None:
            adjacent_vertex = current_node.getValue()
            if not adjacent_vertex.isVisited():
                unvisited_node = adjacent_vertex
            else:
                current_node = current_node.getNext()
        return unvisited_node

    def __str__(self):
        return str(self._label)
