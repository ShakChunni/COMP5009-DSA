import math
from common.DSALinkedList import DSALinkedList
from CollectionRequest import CollectionRequest
from module3_heap.DSAHeap import DSAHeap


class CollectionScheduler:
    def __init__(self, farms, graph, hub="HUB", capacity=100):
        graph.getVertex(hub)
        self.farms = farms
        self.graph = graph
        self.hub = hub
        self.heap = DSAHeap(capacity)
        self.history = DSALinkedList()

    def calculateRequest(self, request_id, farm_id, feedstock):
        request = CollectionRequest(request_id, farm_id, feedstock)
        self.farms.search(farm_id)
        time, path = self.graph.dijkstra(farm_id, self.hub)
        if not math.isfinite(time):
            raise ValueError("No valid collection route to the hub for " + farm_id)
        if time <= 0:
            raise ValueError("Collection transportation time must be greater than zero")
        priority = request.feedstock / time
        if not math.isfinite(priority) or priority <= 0:
            raise ValueError("Calculated priority must be positive and finite")
        request.transport_time = time
        request.path = path
        request.priority = priority
        return request

    def insert(self, request_id, farm_id, feedstock):
        # History includes extracted requests: request IDs cannot be reused.
        for previous in self.history:
            if previous.request_id == request_id:
                raise ValueError("Duplicate collection request ID: " + str(request_id))
        # Avoid accidentally scheduling the same farm twice at the same time.
        for pending in self.heap.entries():
            if pending.farm_id == farm_id:
                raise ValueError("Farm already has a pending collection request: " + farm_id)
        request = self.calculateRequest(request_id, farm_id, feedstock)
        print(f"PRIORITY {request.request_id}: {request.feedstock:.2f} / "
              f"{request.transport_time:.2f} = {request.priority:.6f}")
        self.heap.insert(request)
        request.status = "PENDING"
        self.history.insertLast(request)
        return request

    def _discardDeletedTop(self):
        # A farm may be deleted after scheduling. Check again before collection.
        while not self.heap.isEmpty():
            request = self.heap.peek()
            try:
                self.farms.search(request.farm_id)
                return
            except KeyError:
                removed = self.heap.extract_priority()
                removed.status = "CANCELLED"
                print(f"CANCELLED {removed.request_id}: farm record has been deleted")

    def peek(self):
        self._discardDeletedTop()
        return self.heap.peek()

    def extract_priority(self):
        self._discardDeletedTop()
        request = self.heap.extract_priority()
        request.status = "COLLECTED"
        print("COLLECT:", request)
        return request
