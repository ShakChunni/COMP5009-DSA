from common.DSALinkedList import DSALinkedList


class DSAGraphEdge:
    def __init__(self, destination, weight):
        self.destination = destination
        self.weight = weight


class DSAGraphNode:
    def __init__(self, label, value, index):
        self.label = label
        self.value = value
        self.index = index
        self.adjacent = DSALinkedList()

    def hasEdge(self, other):
        for edge in self.adjacent:
            if edge.destination is other:
                return True
        return False
