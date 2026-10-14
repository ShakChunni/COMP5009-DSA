# Final code check

This checks the functional code against the visible assignment brief. The report
will be checked separately. It does not assert a guaranteed grade.

## Outcome

- Menu moved entirely into `main.py`; `interactive_menu.py` removed.
- Full standard run: **343 PASS checks**, seven suites including benchmarks,
  and all **18** sorting size/condition/algorithm combinations.
- Both 1,000-record sorted exports and the 12-record integrated export independently
  checked for record count and ascending transportation time.
- A fresh package copy launched from another working directory and exercised every
  menu option, both sort/export choices, recovery from invalid data, and clean exit.
- Three fresh independent hostile reviews found no remaining ordinary functional
  defect or unnecessary production feature after the fix below.

## Last review findings resolved

1. **Farm inserted before graph location:** benchmark previously stopped on the
   missing vertex. It now skips hash-only/isolated farms and includes them after
   they are connected. Four sorting-driver regression checks cover that workflow.
2. **CSV parser errors:** `main.py` now handles `csv.Error` at startup and during
   menu operations. An oversized CSV field is tested without crashing the menu.
3. **Menu rename and package instructions:** README/guide updated to `main.py`,
   and ZIP instructions explicitly include every root support dependency.

## Visible functional coverage

| Area | Confirmed |
|---|---|
| Graph | Own weighted undirected adjacency list; 41 vertices/55 edges; cycles and isolated farm; BFS levels; DFS cycle locations/all components; Dijkstra path/time; invalid/unreachable handling |
| Hash | 40 complete source farm records; modulo double hashing; prime capacity; collision probes; insert/search/delete; tombstones; load every 10 inserts; growth 53→107; validation |
| Heap | Computed F/T from hash+Dijkstra; own array max heap; peek/percolating insert/extract; 12 valid insertions/5+ extractions; all array traces; empty/duplicate/invalid/missing/unreachable/zero/deleted-farm cases |
| Sorting | Own stable top-down Merge Sort and median-of-three Hoare Quick Sort; ascending T; 100/500/1000; random/exact 10% identity displacement/reversed; fixed seed; all timing results |
| Integration | Shared farm lookup/graph/scheduler; accepted request history; both sorts and CSV export |
| Error handling | Invalid IDs/names/coordinates/weights/feedstock; duplicate/missing records; CSV/header/row/parser errors; menu recovery/EOF; no third-party runtime dependencies |

Independent review also compared random graph shortest paths to an oracle,
hash operations to a model, heap order/FIFO ties to expected sequences, and both
sorts on adversarial inputs. These review scripts were temporary; reproducible
assignment scenarios and regressions are retained in the submitted drivers.

## Submission matters still outside this code check

- Add required author/date/purpose headers (omitted at the user's earlier request).
- Confirm source-data collection/verification acceptance: the 40 exact rows were
  selected from the supplied sample, not independently collected from the website.
- Check the omitted graph rubric/Sections 10–12 and extra unit restrictions,
  including whether indexed Python lists may serve as arrays.
- The brief's ZIP example names `interactive_menu.py`; this version intentionally
  uses `main.py`, as requested, and documents its interactive entry-point role.
- Include final technical report PDF with Declaration of Originality first.
- Package with the complete dependencies described in README, then submit through
  both required Blackboard links.
