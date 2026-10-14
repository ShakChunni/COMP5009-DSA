from DataLoader import ROOT, buildSystem, loadRequests
from CollectionScheduler import CollectionScheduler
from TestHelpers import check, expectError


def runTests():
    records, farms, graph, scheduler = buildSystem()
    print("=== REQUIRED INTEGRATED HEAP RUN ===")
    accepted, rejected = loadRequests(scheduler, ROOT / "data/collection_requests.csv")
    check("12 accepted insertions and 7 rejected requests", accepted == 12 and rejected == 7)
    check("heap property after insertion run", scheduler.heap.validateHeap())
    count = scheduler.heap.getCount()
    print("PEEK:", scheduler.peek())
    check("peek preserves heap count", scheduler.heap.getCount() == count)
    previous = float("inf")
    for index in range(5):
        request = scheduler.extract_priority()
        print(f"Collection order {index + 1}: {request.request_id}")
        check("non-increasing priority", request.priority <= previous)
        check("heap property after extraction", scheduler.heap.validateHeap())
        previous = request.priority
    while not scheduler.heap.isEmpty():
        request = scheduler.extract_priority()
        check("remaining priorities descending", request.priority <= previous)
        previous = request.priority
    expectError("empty scheduler peek", ValueError, scheduler.peek)
    expectError("empty scheduler extraction", ValueError, scheduler.extract_priority)
    expectError("reused completed request ID", ValueError,
                lambda: scheduler.insert("R001", records.peekFirst().farm_id, 12))
    for value in (0, -1, "bad", None, True, float("nan"), float("inf")):
        expectError(f"invalid feedstock {value}", ValueError,
                    lambda value=value: scheduler.insert("INVALID", records.peekFirst().farm_id, value))
    expectError("empty request ID", ValueError, lambda: scheduler.insert("", records.peekFirst().farm_id, 10))
    expectError("oversized feedstock integer", ValueError,
                lambda: scheduler.insert("HUGE", records.peekFirst().farm_id, 10 ** 1000))
    expectError("invalid direct heap request", ValueError, lambda: scheduler.heap.insert(None))

    print("=== EQUAL PRIORITY FIFO TIES ===")
    first = records.peekFirst()
    second = records.head.getNext().getValue()
    time1, _ = graph.dijkstra(first.farm_id, "HUB")
    time2, _ = graph.dijkstra(second.farm_id, "HUB")
    scheduler.insert("TIE1", first.farm_id, time1)
    scheduler.insert("TIE2", second.farm_id, time2)
    check("equal priority earliest first", scheduler.extract_priority().request_id == "TIE1")
    check("equal priority second next", scheduler.extract_priority().request_id == "TIE2")

    print("=== FARM DELETED AFTER SCHEDULING ===")
    scheduler.insert("DELETED", first.farm_id, 100)
    farms.delete(first.farm_id, trace=True)
    expectError("deleted pending farm cancelled by peek", ValueError, scheduler.peek)
    check("cancelled request removed from heap", scheduler.heap.isEmpty())
    expectError("request for deleted farm", KeyError, lambda: scheduler.insert("AFTERDELETE", first.farm_id, 10))
    farms.insert(first)
    scheduler.insert("DELETED2", first.farm_id, 100)
    farms.delete(first.farm_id)
    expectError("deleted pending farm cancelled by extraction", ValueError, scheduler.extract_priority)
    farms.insert(first)

    # Same-location shortest path is zero, despite all edge weights being positive.
    zero_time_scheduler = CollectionScheduler(farms, graph, hub=first.farm_id)
    expectError("zero transportation time", ValueError,
                lambda: zero_time_scheduler.insert("ZERO", first.farm_id, 10))
    small = CollectionScheduler(farms, graph, capacity=1)
    small.insert("FULL1", first.farm_id, 10)
    expectError("full heap", ValueError, lambda: small.insert("FULL2", second.farm_id, 10))
    check("failed insertion does not enter history", small.history.count() == 1)
    print("HEAP TESTS PASSED")


if __name__ == "__main__":
    runTests()
