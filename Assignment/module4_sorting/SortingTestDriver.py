import random
from CollectionRequest import CollectionRequest
from FarmRecord import FarmRecord
from DataLoader import buildSystem
from module4_sorting.DSAsorts import mergeSort, quickSort, isSorted
from module4_sorting.benchmark import makeRecords, makeCondition, sameRecords, reachableFarmIDs, SEED
from TestHelpers import check


def fixture(values):
    records = [None] * len(values)
    for index, value in enumerate(values):
        request = CollectionRequest(f"TEST{index}", "testfarm", 10)
        request.transport_time = value
        records[index] = request
    return records


def runTests():
    print("=== SORTING EDGE CASES (SYNTHETIC UNIT FIXTURES) ===")
    cases = ((), (1,), (2, 1), (1, 2), (3, 1, 2), (2, 2, 2),
             (5, 4, 3, 2, 1), (1, 2, 3, 4, 5), (1.5, 0.5, 1.5, 2.5))
    for values in cases:
        original = fixture(values)
        for algorithm in (mergeSort, quickSort):
            working = original[:]
            algorithm(working)
            check(f"{algorithm.__name__} {values}", isSorted(working) and sameRecords(original, working))
    repeated = fixture((2, 1, 2, 1, 2, 1))
    mergeSort(repeated)
    check("Merge Sort preserves equal-key order",
          tuple(record.request_id for record in repeated) == ("TEST1", "TEST3", "TEST5", "TEST0", "TEST2", "TEST4"))
    large = fixture((1,) * 1500)
    quickSort(large)
    check("Quick Sort all-equal large input terminates", isSorted(large))

    print("=== REQUIRED GRAPH-DERIVED INPUT CONDITIONS ===")
    _, _, _, scheduler = buildSystem()
    for size in (100, 500, 1000):
        base = makeRecords(scheduler, size, random.Random(SEED + size))
        for condition in ("random", "nearly_sorted", "reversed"):
            inputs = makeCondition(base, condition, random.Random(SEED))
            if condition == "nearly_sorted":
                baseline = base[:]
                mergeSort(baseline)
                moved = sum(inputs[index] is not baseline[index] for index in range(size))
                check(f"{size}: exactly 10% records displaced", moved == size // 10)
            if condition == "reversed":
                check(f"{size}: reversed descending",
                      all(inputs[index - 1].transport_time >= inputs[index].transport_time
                          for index in range(1, size)))
            for algorithm in (mergeSort, quickSort):
                working = inputs[:]
                algorithm(working)
                check(f"{size} {condition} {algorithm.__name__}",
                      isSorted(working) and sameRecords(inputs, working))
    # Synthetic fixture for a normal menu workflow: insert farm before graph node.
    before = reachableFarmIDs(scheduler.farms, scheduler.graph, scheduler.hub)
    extra = FarmRecord("new01", "Test farm without a graph location", "Pigs", -32, 116,
                       "", "", "", "WA", "", "Australia")
    scheduler.farms.insert(extra)
    after = reachableFarmIDs(scheduler.farms, scheduler.graph, scheduler.hub)
    check("benchmark ignores farms whose graph locations are not yet added", before == after)
    generated = makeRecords(scheduler, 100, random.Random(SEED))
    check("benchmark records still generate after farm-only insertion",
          len(generated) == 100 and all(request.farm_id != extra.farm_id for request in generated))
    scheduler.graph.addVertex(extra.farm_id, extra.name)
    check("benchmark also ignores newly added isolated farm locations",
          reachableFarmIDs(scheduler.farms, scheduler.graph, scheduler.hub) == before)
    scheduler.graph.addEdge(extra.farm_id, scheduler.hub, 10)
    check("benchmark includes farm after it is connected to hub",
          extra.farm_id in reachableFarmIDs(scheduler.farms, scheduler.graph, scheduler.hub))
    print("SORTING TESTS PASSED")


if __name__ == "__main__":
    runTests()
