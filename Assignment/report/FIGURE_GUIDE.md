# Figure placement and Overleaf guide

Eight figures were generated with Matplotlib from the saved assignment evidence.
Each has a vector **PDF** for Overleaf and a **300 dpi PNG** for preview/sharing.
Files are under `report/figures/`; `all_figures_preview.pdf` lets you inspect the set.
Use individual PDFs in the report, not the preview compilation.

The **UML/module interaction diagram is explicitly required** by Section 8 and
the report rubric. The other figures support explanations and results; the brief
does not require eight figures. The sorting timing **table** remains required even
when you include its plot. Do not add every supporting figure if it makes the report
repetitive; retain the most useful ones and place extra traces in an appendix.

## Style matched to your paper

The palette was extracted from RGB drawing operators in the supplied
`Containement_Not_Recovery (1).pdf`, then checked against its plotted figures:

| Colour | Hex | Use in assignment figures |
|---|---|---|
| Blue | `#2F5597` | Graph/normal data, Merge Sort |
| Burnt orange | `#C55A11` | Hub/route/root/first five extractions, Quick Sort |
| Green | `#548235` | Hash module/collision record and detected cycle |
| Purple | `#8064A2` | Scheduler/request model and isolated/unreachable farm |

Different figure types use colours for their own labelled categories; legends make
those categories explicit. Serif text, thin outlines, white backgrounds and light
grey grids follow the paper's restrained plotting style. Line markers distinguish
the two sorting algorithms as well as colour. Figures contain no copied source-paper
results. Their underlying values come entirely from the assignment's saved evidence.

## Recommended report order and placement

Use these filenames as identifiers. LaTeX assigns figure numbers automatically,
so do not manually write "Figure 8" merely because a file starts with `08`.

| File stem (PDF and PNG) | Report section / placement | Role |
|---|---|---|
| `01_system_uml` | **System design**, immediately after introducing the four modules, before individual algorithm sections | Required UML/module interaction figure |
| `02_module_data_flow` | **System design / integration**, after explaining how a request moves through lookup, routing and scheduling | Supporting process overview; omit if the UML and prose are sufficient |
| `03_farm_network` | **Graph module**, after dataset/hub/topology assumptions and before discussing BFS/DFS/Dijkstra results | Full network + worked shortest-route example |
| `04_bfs_levels` | **Graph results**, immediately after explaining BFS levels | Optional detailed BFS evidence; appendix if space is limited |
| `05_hash_behaviour` | **Hash module**, after double hashing/tombstone/resizing explanation | Collision resolution and measured load-factor checkpoints |
| `06_max_heap` | **Heap module**, after explaining the heap property and priority calculation | State after the 12th accepted insertion |
| `07_collection_order` | **Scheduling results**, after the heap state and before discussing edge cases | Optional visual collection order; pairs with the F/T table |
| `08_sorting_timings` | **Sorting results**, beside or immediately after the required timing table, before the performance discussion | All algorithms/sizes/conditions from the saved benchmark |

For a concise report, prioritize **01, 03, 05, 06 and 08**. Figures 02, 04 and 07
are useful supporting material, not separate compulsory rubric deliverables.

## Captions, interpretation and source files

### 01 — UML/module interaction

**Suggested caption:**

> Implemented classes and interaction of the four modules. CollectionScheduler
> retrieves FarmRecord information through DSAHashTable and shortest-path results
> through DSAGraph, owns the pending-request DSAHeap, and retains CollectionRequest
> history for the sorting module. DSAsorts.py contains functions rather than a class.

**Discuss:** attributes versus operations; scheduler dependencies; heap ownership;
custom structures. The diagram is intentionally focused on integration rather than
every helper class. Arrow labels identify the dependency/data exchange; the filled
diamond denotes the scheduler owning its heap.

**Basis:** `CollectionScheduler.py`, `CollectionRequest.py`, and the four module
implementations. It is not inferred from timings or generated model requests.

**Label:** `fig:system-uml`. Recommended width: `\linewidth` in a single-column report.

### 02 — Module data flow

**Suggested caption:**

> Data flow from farm and model-network inputs to collection scheduling and reporting.
> A request supplies feedstock F and FarmID; hash lookup and Dijkstra supply the farm
> record and shortest time T. The scheduler calculates P=F/T and inserts a request
> into the max heap. Accepted request history is sorted by ascending T and exported
> to CSV, with statuses updated as requests are processed.

**Discuss:** actual integration rather than four independent demonstrations. The
history includes pending, collected and cancelled accepted requests. The diagram
shows processing stages, not concurrent threads or a separate database server.

**Basis:** `DataLoader.py`, `CollectionScheduler.py`, `main.py`.

**Label:** `fig:module-flow`. Recommended width: `\linewidth`.

### 03 — Full graph and Dijkstra route

**Suggested caption:**

> Educational transportation network with 41 vertices and 55 undirected weighted
> connections. Panel (a) is a schematic: orange highlights the R005 shortest route,
> green the detected cycle, and 404a0 is deliberately isolated. Panel (b) lists the
> R005 farm-to-hub route and its estimated edge times, totaling 874.66 minutes.
> Layout distances are not geographic distances; connections and times are model estimates.

**Discuss:** HUB plus 40 farms, each undirected edge stored twice in code but drawn
once here; cycles provide alternate paths; isolated farm tests unreachable handling.
Grey connections have their exact weights in the submitted transport CSV and graph
trace; only the worked route's weights are labelled to keep the full graph legible.

R005 route: **fzccd → 58yzc → qlctx → v75pu → HUB**. Times:
**291.18 + 200.78 + 183.63 + 199.07 = 874.66 minutes**. The script verifies that
the displayed edge sum matches the saved Dijkstra result. Do not substitute a
straight-line distance for this route total. The large estimate reflects our
educational topology and assumptions, not validated truck travel time.

Detected cycle shown: **a30b2 → c6748 → c1c13 → a30b2**. Isolation is a property
of our test graph, not a claim about real-world road access at Mogumber Piggery.

**Sources:** `figure_data/graph_vertices.csv`, `../data/transport_edges.csv`,
`figure_data/priorities_and_collection_order.csv`.

**Label:** `fig:farm-network`. Use full width; small labels need room. In a
two-column template use a `figure*` rather than shrinking it to one narrow column.

### 04 — BFS levels

**Suggested caption:**

> BFS from HUB groups all 40 reachable vertices, including HUB, by minimum edge count.
> Levels 0–6 contain the connected component. Farm 404a0 is outside these levels
> because it is isolated in the model. BFS levels do not minimize weighted travel time.

**Discuss:** level 0 is HUB, level 1 is directly connected locations, later levels
require more connections. Level membership is not a ranking of feedstock priority.
The list preserves actual BFS output order within each level.

**Sources:** `figure_data/bfs_levels.csv`, `figure_data/graph_vertices.csv`.

**Label:** `fig:bfs-levels`. Recommended width: `\linewidth`; suitable for an appendix.

### 05 — Hash collision and load factor

**Suggested caption:**

> Double-hashing collision resolution and resizing. Panel (a) shows selected slots
> in a 53-slot table: qlctx and c1c13 both hash initially to 45; c1c13 probes to 44.
> Deleting qlctx leaves a tombstone, so search continues from 45 to 44. Reinsertion
> reuses slot 45. Panel (b) shows live-record load factors from the 40-record run;
> capacity grows from 53 to 107 before insertion 38 would exceed 0.7.

**Discuss:** an occupied slot differs from FREE and DELETED; double hashing is not
linear probing and need not move to slot 46. A tombstone must not stop a search.
The 53-slot collision demonstration is a separate small table from the resizing
run; do not interpret it as a snapshot of the final 107-slot table.

Requested checkpoints: **10/53**, **20/53**, **30/53**, **40/107**. The plot also
shows actual insertion states **37/53** and **38/107** to reveal the resize.
Its threshold is checked before insertion, so the table does not first grow above 0.7.
Lines join checkpoints and do not imply intermediate loads were all measured/displayed.

**Source:** `../sample_output/hash_tests.txt`. The script reads the explicit collision
and logged capacities; exact loads are computed as count/capacity.

**Label:** `fig:hash-behaviour`. Recommended width: `\linewidth`.

### 06 — Max heap after insertion 12

**Suggested caption:**

> Array-based max heap after 12 accepted collection-request insertions. Nodes show
> RequestID and calculated P=F/T; i labels each underlying array index. Parent
> priority is at least that of either child, placing R011 at the root. Children
> occupy indices 2i+1 and 2i+2. This is heap storage order, not a fully sorted sequence.

**Discuss:** why the root is returned by peek/extract; why percolation is necessary;
why a left-to-right reading of all nodes is not collection order. Equal priorities
use FIFO sequence, although this displayed state does not contain an equal-priority tie.
The script checks the parent/child property of the saved state before plotting.

**Source:** `figure_data/heap_states.csv`, operation 12, insertion.

**Label:** `fig:max-heap`. Recommended width: `\linewidth`.

### 07 — Calculated collection order

**Suggested caption:**

> Calculated priority order for the 12 accepted requests, using P=F/T in model
> tonnes per minute. Orange identifies the first five required extractions:
> R011, R003, R004, R001 and R009. Remaining requests appear in blue. Quantities
> and transportation times are educational modelling data.

**Discuss:** a larger F improves priority and a larger T reduces it. A nearby farm
with less feedstock may outrank a distant farm with more. The order is different
from reporting order, which is ascending T. Use the F/T table in RESULTS alongside
this plot to justify calculations; the plot alone does not show both inputs.

**Source:** `figure_data/priorities_and_collection_order.csv`.

**Label:** `fig:collection-order`. Recommended width: `\linewidth`; optional appendix figure.

### 08 — Sorting timings

**Suggested caption:**

> Mean sorting time for Merge Sort and Quick Sort at 100, 500 and 1,000 collection
> records under random, nearly sorted (10% of record identities displaced) and
> reversed inputs. Both algorithms receive the same input for each case. Means
> use seven measured repetitions after warm-up, with base seed 5008. Data generation,
> input copying, verification and export are excluded from timing; transport keys
> derive from the graph's shortest-path results.

**Discuss:** growth with size; input-condition differences; repeated T keys;
median-of-three pivot; stable Merge versus unstable Quick; theoretical versus observed
performance; timing noise. The graph shows this local run, not a universal speed
ranking or proof of asymptotic complexity. There are no invented error bars: only
means are saved. Reversed input need not be worst-case for this Quick Sort.

**Sources:** `../sample_output/benchmark_results.csv`, `benchmark_environment.json`.
All 18 means are plotted. Include the **required numerical results table** from
RESULTS too. Report the saved Python/platform/timer details in the methods paragraph.

**Label:** `fig:sorting-timings`. Use full width; `figure*` in two-column layouts.

## Overleaf use

Upload the individual PDFs you choose into an Overleaf `figures/` folder. Also add
the table from RESULTS and your references. Minimum packages:

```tex
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage[hidelinks]{hyperref}
```

Example figure block (paste after the paragraph introducing the figure):

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{figures/01_system_uml.pdf}
  \caption{Implemented classes and interaction of the four modules.
  CollectionScheduler retrieves farm information through DSAHashTable and
  shortest-path results through DSAGraph, owns the pending-request DSAHeap,
  and retains CollectionRequest history for the sorting module.}
  \label{fig:system-uml}
\end{figure}
```

Use `Figure~\ref{fig:system-uml}` in prose. In a two-column template, wide diagrams
and the three-panel benchmark fit better in `figure*` with `width=\textwidth`.
Single-column reports can keep `figure` with `width=\linewidth`. Allow LaTeX to float
figures close to their first discussion instead of forcing every one with `[H]`.
Keep captions outside the image, explain symbols/units, and check the compiled PDF
for readable text. Copy-and-paste captions above are starting text to adapt to your
own report and referencing style, not a substitute for analysing the results.

## Regeneration and reproducibility

Plotting does not rerun the experiment or change the core application. After a code
or data change, regenerate evidence and then figures:

```sh
python3 run_tests.py
# In a Python environment containing matplotlib:
python3 report/generate_figures.py
```

The core application and tests use only the standard library. The optional plotting
helper requires Matplotlib (listed in `requirements-figures.txt`). For an isolated
environment, from Assignment/:

```sh
python3 -m venv /tmp/comp5008-figures-env
/tmp/comp5008-figures-env/bin/python -m pip install -r report/requirements-figures.txt
/tmp/comp5008-figures-env/bin/python report/generate_figures.py
```

`figures_manifest.json` records palette, Matplotlib version and SHA-256 hashes of
the input evidence. If benchmarks are rerun, timings/RESULTS change: regenerate the
plot rather than presenting old figures alongside a new table. The source reference
paper is not needed to regenerate these figures; its extracted palette is stored
in the plotting script.

## Submission

The final PDF report should embed the chosen figures. Including `report/figures/`,
this guide and the plotting script in the ZIP is optional supporting material;
they do not replace the report PDF, test traces or required benchmark table. Keep
the reference paper outside the assignment ZIP unless your unit specifically asks
for it. The figure generator's dependency does not change how `python3 main.py`
or `python3 run_tests.py` works.
