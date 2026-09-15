from DSALinkedList import DSALinkedList, DSAListNode
from DSAGraphNode import DSAGraphNode
from DSAQueue import DSAQueue
from DSAStack import DSAStack


class DSAGraph:
    def __init__(self):
        self._vertices = DSALinkedList()
        self._count = 0
        self._edge_count = 0

    def isEmpty(self):
        return self._count == 0

    def getVertexCount(self):
        return self._count

    def getEdgeCount(self):
        return self._edge_count

    def hasVertex(self, label):
        current_node = self._vertices.head
        found = False
        target_label = str(label)
        while current_node is not None and not found:
            if current_node.getValue().getLabel() == target_label:
                found = True
            else:
                current_node = current_node.getNext()
        return found

    def getVertex(self, label):
        current_node = self._vertices.head
        found_vertex = None
        target_label = str(label)
        while current_node is not None and found_vertex is None:
            if current_node.getValue().getLabel() == target_label:
                found_vertex = current_node.getValue()
            else:
                current_node = current_node.getNext()

        if found_vertex is None:
            raise KeyError("Vertex not found: " + target_label)

        return found_vertex

    def addVertex(self, label, value=None):
        target_label = str(label)
        if self.hasVertex(target_label):
            raise ValueError("Vertex already exists: " + target_label)

        new_vertex = DSAGraphNode(target_label, value)

        if self._vertices.isEmpty():
            self._vertices.insertLast(new_vertex)
        elif target_label < self._vertices.head.getValue().getLabel():
            self._vertices.insertFirst(new_vertex)
        elif target_label > self._vertices.tail.getValue().getLabel():
            self._vertices.insertLast(new_vertex)
        else:
            scan_node = self._vertices.head
            inserted = False
            while scan_node is not None and not inserted:
                if target_label < scan_node.getValue().getLabel():
                    new_list_node = DSAListNode(new_vertex)
                    previous_node = scan_node.getPrev()
                    previous_node.setNext(new_list_node)
                    new_list_node.setPrev(previous_node)
                    new_list_node.setNext(scan_node)
                    scan_node.setPrev(new_list_node)
                    inserted = True
                else:
                    scan_node = scan_node.getNext()

        self._count += 1

    def addEdge(self, label_one, label_two):
        try:
            vertex_one = self.getVertex(label_one)
        except KeyError:
            self.addVertex(label_one)
            vertex_one = self.getVertex(label_one)

        try:
            vertex_two = self.getVertex(label_two)
        except KeyError:
            self.addVertex(label_two)
            vertex_two = self.getVertex(label_two)

        if not vertex_one.hasEdge(vertex_two):
            vertex_one.addEdge(vertex_two)
            vertex_two.addEdge(vertex_one)
            self._edge_count += 1

    def deleteEdge(self, label_one, label_two):
        vertex_one = self.getVertex(label_one)
        vertex_two = self.getVertex(label_two)

        if vertex_one.hasEdge(vertex_two):
            vertex_one.deleteEdge(vertex_two)
            vertex_two.deleteEdge(vertex_one)
            self._edge_count -= 1
        else:
            raise KeyError("Edge not found between " + str(label_one) + " and " + str(label_two))

    def deleteVertex(self, label):
        target_vertex = self.getVertex(label)

        current_node = self._vertices.head
        while current_node is not None:
            vertex = current_node.getValue()
            if vertex.hasEdge(target_vertex):
                vertex.deleteEdge(target_vertex)
                self._edge_count -= 1
            current_node = current_node.getNext()

        self._vertices.delete(target_vertex)
        self._count -= 1

    def isAdjacent(self, label_one, label_two):
        vertex_one = self.getVertex(label_one)
        vertex_two = self.getVertex(label_two)
        return vertex_one.hasEdge(vertex_two)

    def getAdjacent(self, label):
        vertex = self.getVertex(label)
        return vertex.getAdjacent()

    def displayAsList(self):
        result = ""
        current_node = self._vertices.head
        while current_node is not None:
            vertex = current_node.getValue()
            result += vertex.getLabel() + " | "

            adjacent_list = vertex.getAdjacent()
            adjacent_node = adjacent_list.head
            is_first = True
            while adjacent_node is not None:
                if not is_first:
                    result += ", "
                result += adjacent_node.getValue().getLabel()
                is_first = False
                adjacent_node = adjacent_node.getNext()

            result += "\n"
            current_node = current_node.getNext()
        return result

    def displayAsMatrix(self):
        labels = []
        current_node = self._vertices.head
        while current_node is not None:
            labels.append(current_node.getValue().getLabel())
            current_node = current_node.getNext()

        result = "   "
        index = 0
        while index < len(labels):
            result += " " + labels[index] + " "
            index += 1
        result += "\n"

        row_index = 0
        while row_index < len(labels):
            row_label = labels[row_index]
            row_vertex = self.getVertex(row_label)
            result += " " + row_label + " "

            col_index = 0
            while col_index < len(labels):
                col_label = labels[col_index]
                col_vertex = self.getVertex(col_label)
                if row_vertex.hasEdge(col_vertex):
                    result += " 1 "
                else:
                    result += " 0 "
                col_index += 1

            result += "\n"
            row_index += 1

        return result

    def breadthFirstSearch(self, start_label=None):
        if self.isEmpty():
            raise ValueError("Graph is empty")

        tree_edges = DSAQueue()
        queue = DSAQueue()

        current_node = self._vertices.head
        while current_node is not None:
            current_node.getValue().clearVisited()
            current_node = current_node.getNext()

        if start_label is not None:
            start_vertex = self.getVertex(start_label)
        else:
            start_vertex = self._vertices.head.getValue()

        start_vertex.setVisited()
        queue.enqueue(start_vertex)

        while not queue.isEmpty():
            current_vertex = queue.dequeue()

            adjacent_node = current_vertex.getAdjacent().head
            while adjacent_node is not None:
                neighbor = adjacent_node.getValue()
                if not neighbor.isVisited():
                    tree_edges.enqueue(current_vertex.getLabel())
                    tree_edges.enqueue(neighbor.getLabel())
                    neighbor.setVisited()
                    queue.enqueue(neighbor)
                adjacent_node = adjacent_node.getNext()

        return tree_edges

    def depthFirstSearch(self, start_label=None):
        if self.isEmpty():
            raise ValueError("Graph is empty")

        tree_edges = DSAQueue()
        stack = DSAStack()

        current_node = self._vertices.head
        while current_node is not None:
            current_node.getValue().clearVisited()
            current_node = current_node.getNext()

        if start_label is not None:
            start_vertex = self.getVertex(start_label)
        else:
            start_vertex = self._vertices.head.getValue()

        start_vertex.setVisited()
        stack.push(start_vertex)
        current_vertex = start_vertex

        while not stack.isEmpty():
            unvisited_neighbor = current_vertex.getUnvisitedAdjacent()
            while unvisited_neighbor is not None:
                tree_edges.enqueue(current_vertex.getLabel())
                tree_edges.enqueue(unvisited_neighbor.getLabel())
                unvisited_neighbor.setVisited()
                stack.push(unvisited_neighbor)
                current_vertex = unvisited_neighbor
                unvisited_neighbor = current_vertex.getUnvisitedAdjacent()

            current_vertex = stack.pop()

        return tree_edges
