import csv
import json
import platform
import random
import time
from DataLoader import ROOT, buildSystem, writeCollectionRecords
from module4_sorting.DSAsorts import mergeSort, quickSort, isSorted

SEED = 5008
REPETITIONS = 7


def reachableFarmIDs(farms, graph, hub):
    identifiers = [None] * farms.getCount()
    count = 0
    for farm in farms.records():
        # A farm may be added to the lookup table before its graph location.
        if not graph.hasVertex(farm.farm_id):
            continue
        minutes, _ = graph.dijkstra(farm.farm_id, hub)
        if minutes != float("inf") and minutes > 0:
            identifiers[count] = farm.farm_id
            count += 1
    return identifiers[:count]


def makeRecords(scheduler, size, generator):
    identifiers = reachableFarmIDs(scheduler.farms, scheduler.graph, scheduler.hub)
    if not identifiers:
        raise ValueError("No reachable farms available for sorting records")
    records = [None] * size
    for index in range(size):
        farm_id = identifiers[generator.randrange(len(identifiers))]
        records[index] = scheduler.calculateRequest(f"B{size}_{index:04}", farm_id,
                                                   generator.randint(5, 50))
    return records


def shuffleArray(array, generator):
    # Fisher-Yates shuffle; reproducible without using a built-in sort.
    for index in range(len(array) - 1, 0, -1):
        other = generator.randrange(index + 1)
        array[index], array[other] = array[other], array[index]


def makeCondition(base, condition, generator):
    records = base[:]
    if condition == "random":
        shuffleArray(records, generator)
    elif condition in ("nearly_sorted", "reversed"):
        mergeSort(records)
        if condition == "reversed":
            for index in range(len(records) // 2):
                other = len(records) - index - 1
                records[index], records[other] = records[other], records[index]
        else:
            # Select 10% distinct positions, then swap in disjoint pairs.
            count = len(records) // 10
            if count % 2 != 0:
                raise ValueError("Nearly-sorted generation requires an even displacement count")
            positions = [None] * len(records)
            for index in range(len(records)):
                positions[index] = index
            shuffleArray(positions, generator)
            for index in range(0, count, 2):
                first, second = positions[index], positions[index + 1]
                records[first], records[second] = records[second], records[first]
    else:
        raise ValueError("Unknown input condition")
    return records


def sameRecords(before, after):
    """Check identity preservation independently of the sorting implementations."""
    if len(before) != len(after):
        return False
    for original in before:
        matches = 0
        for candidate in after:
            if candidate is original:
                matches += 1
        if matches != 1:
            return False
    return True


def runBenchmarks(scheduler=None):
    if scheduler is None:
        _, _, _, scheduler = buildSystem()
    output = ROOT / "sample_output"
    output.mkdir(exist_ok=True)
    rows = [None] * 18
    row_index = 0
    for size in (100, 500, 1000):
        base = makeRecords(scheduler, size, random.Random(SEED + size))
        for condition_index, condition in enumerate(("random", "nearly_sorted", "reversed")):
            inputs = makeCondition(base, condition, random.Random(SEED + size + condition_index + 1))
            totals = [0.0, 0.0]
            algorithms = (mergeSort, quickSort)
            # Warm-up outside the measured repetitions.
            for algorithm in algorithms:
                algorithm(inputs[:])
            for repetition in range(REPETITIONS):
                # Alternate first algorithm to reduce ordering effects.
                order = (0, 1) if repetition % 2 == 0 else (1, 0)
                for algorithm_index in order:
                    working = inputs[:]  # Fresh copy, made outside timing.
                    start = time.perf_counter_ns()
                    algorithms[algorithm_index](working)
                    elapsed = time.perf_counter_ns() - start
                    totals[algorithm_index] += elapsed / 1_000_000
                    if not isSorted(working) or not sameRecords(inputs, working):
                        raise AssertionError("Sorting correctness/permutation check failed")
            for algorithm_index, name in enumerate(("Merge Sort", "Quick Sort")):
                mean = totals[algorithm_index] / REPETITIONS
                rows[row_index] = (size, condition, name, REPETITIONS, mean)
                row_index += 1
                print(f"{size:4} {condition:14} {name:10} mean={mean:.6f} ms")
            if size == 1000 and condition == "random":
                writeCollectionRecords(output / "sorting_input_1000.csv", inputs)
                for algorithm, filename in ((mergeSort, "merge_sorted_1000.csv"),
                                            (quickSort, "quick_sorted_1000.csv")):
                    working = inputs[:]
                    algorithm(working)
                    writeCollectionRecords(output / filename, working)

    with (output / "benchmark_results.csv").open("w", newline="", encoding="utf-8") as destination:
        writer = csv.writer(destination)
        writer.writerow(("Records", "Condition", "Algorithm", "Repetitions", "MeanMilliseconds"))
        writer.writerows(rows)
    metadata = {"seed": SEED, "repetitions": REPETITIONS,
                "python": platform.python_version(), "platform": platform.platform(),
                "processor": platform.processor(), "timer": "time.perf_counter_ns",
                "farm_records": scheduler.farms.getCount(),
                "vertices": scheduler.graph.getVertexCount(),
                "edges": scheduler.graph.getEdgeCount(),
                "dataset_generation_timed": False, "input_copy_timed": False,
                "verification_timed": False}
    (output / "benchmark_environment.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return rows


if __name__ == "__main__":
    runBenchmarks()
