"""Run the required demonstrations and save readable report evidence."""

import contextlib
from DataLoader import ROOT, buildSystem, loadRequests, writeCollectionRecords
from module1_graph.GraphTestDriver import runTests as graphTests
from module2_hash.HashTestDriver import runTests as hashTests
from module3_heap.HeapTestDriver import runTests as heapTests
from module4_sorting.SortingTestDriver import runTests as sortingTests
from module4_sorting.DSAsorts import mergeSort, quickSort, isSorted
from module4_sorting.benchmark import runBenchmarks, sameRecords
from TestHelpers import check
from generate_report_evidence import main as generateEvidence
from InputTestDriver import runTests as inputTests


def integrationTest():
    _, farms, graph, scheduler = buildSystem()
    accepted, rejected = loadRequests(scheduler, ROOT / "data/collection_requests.csv")
    check("integration input counts", accepted == 12 and rejected == 7)
    for _ in range(5):
        scheduler.extract_priority()
    original = [None] * scheduler.history.count()
    for index, request in enumerate(scheduler.history):
        original[index] = request
        check("request links all modules", farms.search(request.farm_id).farm_id == request.farm_id
              and graph.dijkstra(request.farm_id, scheduler.hub)[0] == request.transport_time
              and request.priority == request.feedstock / request.transport_time)
    merged, quick = original[:], original[:]
    mergeSort(merged)
    quickSort(quick)
    check("both sorting algorithms integrated with request history",
          isSorted(merged) and isSorted(quick) and sameRecords(original, merged)
          and sameRecords(original, quick))
    writeCollectionRecords(ROOT / "sample_output/collection_records_sorted.csv", merged)
    print("INTEGRATION TEST PASSED")


def main():
    output = ROOT / "sample_output"
    output.mkdir(exist_ok=True)
    suites = (("graph_tests.txt", graphTests), ("hash_tests.txt", hashTests),
              ("heap_tests.txt", heapTests), ("sorting_tests.txt", sortingTests),
              ("input_tests.txt", inputTests), ("integration_tests.txt", integrationTest),
              ("benchmark_run.txt", runBenchmarks))
    for filename, suite in suites:
        print("Running", filename)
        with (output / filename).open("w", encoding="utf-8") as log:
            with contextlib.redirect_stdout(log):
                suite()
        print("PASS", filename)
    print("All module tests, integration tests and 18 benchmark combinations passed.")
    generateEvidence()


if __name__ == "__main__":
    main()
