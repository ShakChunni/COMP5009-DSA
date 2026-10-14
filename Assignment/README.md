# COMP5008 Biogas Feedstock Collection Network

Python backend with four integrated modules: weighted graph, farm hash table,
collection max heap, and Merge/Quick Sort reporting. No third-party packages needed.

## Run

From this folder:

```sh
python3 main.py
```

`main.py` contains the interactive menu, matching the practicals. Paths resolve relative to this folder,
so `python3 /absolute/path/to/Assignment/main.py` also works from another directory.
Python 3.10+ is recommended; this version was checked with Python 3.14.3.
`main.py` provides the interactive-entry-point role shown as `interactive_menu.py`
in the brief's folder example.

The menu starts with 40 farms and the graph already loaded, and an empty request
heap. Option 13 loads the collection-request CSV (12 accepted, 7 deliberately invalid).
Use options 10 and 11 to peek/extract; option 14 sorts and saves all accepted requests
by transport time. Repeated CSV loading rejects repeated request IDs.

## Tests and results

```sh
python3 run_tests.py
```

This runs each module's driver, CSV/menu input tests, the integrated scenario and all 18 benchmark
combinations. It saves logs, sorted collection CSVs and timing results in
`sample_output/`, then refreshes `report/RESULTS.md` and `report/figure_data/`.
Failures raise an error and stop the run; inspect the corresponding log.

Individual runs (use `-m` from this folder):

```sh
python3 -m module1_graph.GraphTestDriver
python3 -m module2_hash.HashTestDriver
python3 -m module3_heap.HeapTestDriver
python3 -m module4_sorting.SortingTestDriver
python3 -m module4_sorting.benchmark
python3 InputTestDriver.py
python3 generate_report_evidence.py
```

## Files and responsibilities

| File/folder | Responsibility |
|---|---|
| `main.py` | Entry point and interactive driver |
| `FarmRecord.py` | Farm fields and ID/name/coordinate validation |
| `CollectionRequest.py` | Request fields and feedstock validation |
| `CollectionScheduler.py` | Connects hash lookup, Dijkstra and heap; keeps request history |
| `DataLoader.py` | CSV input, shared system construction and record export |
| `common/` | Own linked list, queue and stack adapted from Practical 6 |
| `module1_graph/` | Weighted adjacency-list graph and test driver |
| `module2_hash/` | Double-hashing table, entries and test driver |
| `module3_heap/` | Array max heap, entries and test driver |
| `module4_sorting/` | Merge Sort, Quick Sort, tests and benchmark |
| `prepare_data.py` | Recreates selected farm CSV and educational modelling CSVs |
| `run_tests.py`, `TestHelpers.py` | Run all demonstrations and check results |
| `generate_report_evidence.py` | Regenerates factual report tables and figure inputs |
| `report/REPORT_GUIDE.md` | Detailed notes for writing your own report in Overleaf |
| `report/RESULTS.md` | Actual results for the latest saved benchmark run |

## Data and assumptions

The original `farm_dataset_sample.csv` is preserved. `data/dataset.csv` selects
the first 40 eligible records in source order: WA, Open, confirmed category/species,
cattle/pigs/sheep/goats, excluding names containing "proposed". Farm IDs and
all source columns are retained. This is a selection from the supplied file,
not an independently harvested or fully verified dataset.

The proposed hub uses illustrative Kwinana-area coordinates (-32.23, 115.78).
Connections follow a documented educational chain/chord pattern. Edge times use
great-circle distance, a 1.3 road factor and 60 km/h. The last selected farm is
deliberately isolated. These are model estimates, not real road-network measurements.
Feedstock quantities are educational model tonnes, not measured waste production.

```sh
python3 prepare_data.py
```

This recreates the three files under `data/`; run it only when you want to reset
them to the original deterministic model. It does not alter the supplied source CSV.

## Programming choices

Core graph adjacency uses our linked list; BFS/DFS use our queue/stack. The hash
table and heap use indexed, preallocated Python lists as arrays; neither uses a
dictionary for core lookup. Sorting is implemented manually. Standard-library CSV
dictionaries only parse fields; JSON dictionaries only store benchmark metadata.
There is no NetworkX, heapq, built-in sorting or third-party numerical library.

Requests use P=F/T with positive F and positive reachable T. A request ID cannot
be reused, and a farm cannot have two pending requests. Ties are FIFO. A request
for a deleted farm is cancelled when it reaches the heap root. Accepted requests
remain in history with PENDING/COLLECTED/CANCELLED status and can be sorted/exported.
Transport times and priorities are snapshots calculated when requests are accepted;
adding graph edges does not automatically recalculate existing requests.
The deletion check uses the current lookup table: if the same FarmID is reinserted
before its pending request reaches the root, that request remains eligible with
its original calculated route/time. An ID that is still missing is cancelled.

Menu insertions/deletions are in memory for that session. Deleting farm information
does not remove its geographic vertex or routes through it. A new farm needs its
graph vertex (option 16) and connections (option 17). CSV export is the record store;
no separate database server is needed by the explicit implementation tasks.
Benchmarks use only farms currently present in the graph with a positive hub route;
new farm records without graph locations or connections are skipped.

## Before submission

- Read the final checklist in `report/REPORT_GUIDE.md`.
- Confirm the supplied sample is acceptable as the farm-data source: the brief says
  to collect data from the website and describes this CSV as an example.
- Check the full brief for removed sections/graph rubric and any extra unit restrictions.
- The brief shows `interactive_menu.py`; this version uses `main.py` at your request.
- Confirm indexed Python lists are allowed as arrays under those unit restrictions.
- Add author/date/purpose headers later; they are currently omitted at your request.
- Produce `technical_report.pdf` with the Declaration of Originality first.
- Package as `COMP5008_assignment_<studentID>.zip` with the matching top-level folder.
- Submit the report to Turnitin AND the ZIP to the separate Blackboard assignment link.

This working folder is not yet a final submission ZIP or technical report PDF.

## ZIP contents

Name the ZIP `COMP5008_assignment_<studentID>.zip` and use the matching top-level
folder. Include:

- `main.py`, `README.md` and **all other root Python files**, including the shared
  models/loaders, test runner, `TestHelpers.py`, `InputTestDriver.py`, data preparation
  and evidence-generation scripts.
- `common/` and all four `module*_*/` folders, with source files, `__init__.py`,
  test drivers and the sorting benchmark.
- `data/` with farm, transport-edge and collection-request CSVs.
- Original `farm_dataset_sample.csv`, because `prepare_data.py` uses it.
- `sample_output/` with operation traces, sorted exports, timings and environment metadata.
- Final `technical_report.pdf`, with Declaration of Originality as its first page.
- `report/` is optional supporting material; the final PDF is required regardless.

Exclude `__pycache__/`, `*.pyc`, `.DS_Store`, `.git/` and temporary/editor files.
The assignment-brief PDF is not needed in the submission ZIP. Keep the module
folders rather than flattening imports. Run `python3 main.py` and `python3 run_tests.py`
from an extracted copy before submitting.
