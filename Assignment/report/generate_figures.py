"""Matplotlib report figures from saved assignment evidence, not new experiments.

This optional report helper needs matplotlib. The application/tests do not.
Palette matched to RGB operators in the supplied Containement_Not_Recovery paper.
"""

import csv
import hashlib
import json
import math
import os
import re
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "comp5008-matplotlib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "report/figures"
BLUE = "#2F5597"
ORANGE = "#C55A11"
GREEN = "#548235"
PURPLE = "#8064A2"
GREY = "#777777"
LIGHT = "#D8D8D8"

plt.rcParams.update({
    "font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.fontsize": 9, "axes.linewidth": 0.7,
    "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.dpi": 300,
})


def readCSV(relative):
    with (ROOT / relative).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def setupChart(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(True, color=LIGHT, linewidth=0.55, linestyle=":")
    ax.set_axisbelow(True)


def arrow(ax, start, end, label="", colour=GREY, style="->", label_at=None,
          connection="arc3,rad=0", width=1.1):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=11,
                                color=colour, linewidth=width, connectionstyle=connection))
    if label:
        point = label_at if label_at else ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        ax.text(*point, label, ha="center", va="center", fontsize=9,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5})


def classBox(ax, x, y, width, height, title, attributes, methods, colour):
    ax.add_patch(Rectangle((x, y), width, height, facecolor="white", edgecolor=colour, linewidth=1.1))
    header = 0.48
    ax.add_patch(Rectangle((x, y + height - header), width, header,
                           facecolor=colour, edgecolor=colour, alpha=0.12))
    ax.plot((x, x + width), (y + height - header,) * 2, color=colour, linewidth=0.8)
    ax.text(x + width / 2, y + height - header / 2, title,
            ha="center", va="center", fontsize=10.5, fontweight="bold")
    attribute_height = 0.30 * len(attributes) + 0.13
    dividing_y = y + height - header - attribute_height
    for index, line in enumerate(attributes):
        ax.text(x + 0.16, y + height - header - 0.22 - index * 0.30,
                line, va="center", fontsize=9.4)
    ax.plot((x, x + width), (dividing_y,) * 2, color=colour, linewidth=0.65)
    for index, line in enumerate(methods):
        ax.text(x + 0.16, dividing_y - 0.22 - index * 0.30,
                line, va="center", fontsize=9.4)


def systemUML():
    fig, ax = plt.subplots(figsize=(8.2, 7.0))
    ax.set(xlim=(0, 14), ylim=(-0.3, 10.6))
    ax.axis("off")
    classBox(ax, 0.3, 7.3, 4.3, 2.65, "DSAGraph (Module 1)",
             ("vertices: own linked list", "weighted undirected adjacency lists"),
             ("+ addVertex(), addEdge()", "+ breadthFirstSearch(), depthFirstSearch()",
              "+ dijkstra(source, destination)"), BLUE)
    classBox(ax, 9.4, 7.3, 4.3, 2.65, "DSAHashTable (Module 2)",
             ("slots: array of DSAHashEntry", "value: complete FarmRecord"),
             ("+ insert(record)", "+ search(FarmID), delete(FarmID)",
              "- _findIndex(), _resize()"), GREEN)
    classBox(ax, 4.65, 3.8, 4.7, 2.85, "CollectionScheduler",
             ("farms, graph, hub", "heap; accepted history: linked list"),
             ("+ calculateRequest(): P = F / T", "+ insert(), peek(), extract_priority()",
              "- _discardDeletedTop()"), PURPLE)
    classBox(ax, 0.3, 0.7, 4.3, 2.65, "DSAHeap (Module 3)",
             ("array of DSAHeapEntry", "priority, request, FIFO sequence"),
             ("+ insert(request)", "+ peek(), extract_priority()",
              "- _higher(first, second)"), ORANGE)
    classBox(ax, 9.4, 0.7, 4.3, 2.65, "DSAsorts.py (Module 4)",
             ("<<module: functions, not a class>>", "key: transport_time ascending"),
             ("+ mergeSort(records)", "+ quickSort(records)",
              ""), BLUE)
    classBox(ax, 4.85, 0.7, 4.3, 2.2, "CollectionRequest",
             ("RequestID, FarmID, feedstock F", "shortest T, path, priority P", "status"),
             (), PURPLE)
    arrow(ax, (4.85, 6.6), (3.7, 7.3), "Dijkstra: T + path", BLUE, label_at=(3.0, 6.65))
    arrow(ax, (9.15, 6.6), (10.3, 7.3), "lookup FarmID", GREEN, label_at=(11.2, 6.65))
    # A filled diamond at the scheduler denotes ownership of its heap.
    ax.add_patch(Polygon(((4.65, 4.65), (4.49, 4.75), (4.33, 4.65), (4.49, 4.55)),
                         closed=True, facecolor=PURPLE, edgecolor=PURPLE))
    arrow(ax, (4.33, 4.65), (3.8, 3.35), "owns pending heap", ORANGE, label_at=(2.45, 4.2))
    arrow(ax, (9.35, 4.6), (10.1, 3.35), "accepted history", BLUE, label_at=(11.5, 4.2), style="->")
    arrow(ax, (7.0, 3.8), (7.0, 2.9), "creates / retains", PURPLE, label_at=(8.0, 3.4))
    ax.text(7, 10.38, "Implemented classes and four-module interaction",
            ha="center", fontsize=12, fontweight="bold")
    ax.text(7, 0.15, "Class compartments show attributes and operations; arrows denote use/data dependencies.",
            ha="center", fontsize=9, color=GREY)
    fig.tight_layout(pad=0.5)
    return fig


def moduleFlow():
    fig, ax = plt.subplots(figsize=(8.2, 4.5))
    ax.set(xlim=(0, 12), ylim=(0, 6.0))
    ax.axis("off")

    def box(x, y, width, height, text, colour):
        ax.add_patch(FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.08",
                                    facecolor="white", edgecolor=colour, linewidth=1.1))
        ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=10)

    box(0.25, 4.6, 2.0, 0.85, "Farm CSV\noriginal IDs", GREEN)
    box(3.0, 4.6, 2.55, 0.85, "Farm hash table\ncomplete record lookup", GREEN)
    box(0.25, 2.9, 2.0, 0.95, "Farm locations +\nmodel edge CSV", BLUE)
    box(3.0, 2.9, 2.55, 0.95, "Weighted graph\nDijkstra: shortest T/path", BLUE)
    box(0.25, 1.15, 2.0, 0.95, "Collection request\nFarmID + feedstock F", PURPLE)
    box(6.1, 2.85, 2.65, 1.05, "Scheduler validates\nand calculates P = F/T", PURPLE)
    box(9.45, 2.85, 2.25, 1.05, "Array max heap\nhighest P first", ORANGE)
    box(6.1, 0.55, 2.65, 1.05, "All accepted requests\nhistory with status", PURPLE)
    box(9.45, 0.55, 2.25, 1.05, "Merge / Quick Sort\nby ascending T", BLUE)
    arrow(ax, (2.33, 5.03), (2.92, 5.03), colour=GREEN)
    arrow(ax, (2.33, 3.38), (2.92, 3.38), colour=BLUE)
    arrow(ax, (5.63, 5.03), (6.7, 3.98), colour=GREEN)
    arrow(ax, (5.63, 3.38), (6.02, 3.38), colour=BLUE)
    arrow(ax, (2.33, 1.63), (6.02, 3.0), colour=PURPLE)
    arrow(ax, (8.83, 3.38), (9.37, 3.38), colour=ORANGE)
    arrow(ax, (7.43, 2.77), (7.43, 1.68), colour=PURPLE)
    arrow(ax, (8.83, 1.08), (9.37, 1.08), colour=BLUE)
    ax.text(10.58, 0.18, "sorted CSV export", ha="center", fontsize=9.5, color=BLUE)
    ax.text(10.58, 4.24, "peek / extract\ncollection order", ha="center", fontsize=9.5, color=ORANGE)
    ax.text(6, 5.85, "Data flow: lookup, routing, scheduling and reporting", ha="center",
            fontsize=12, fontweight="bold")
    fig.tight_layout(pad=0.6)
    return fig


def farmNetwork(vertices, edges, priorities):
    fig = plt.figure(figsize=(9.2, 5.4))
    grid = fig.add_gridspec(1, 2, width_ratios=(3.5, 1.35), wspace=0.20)
    left, right = fig.add_subplot(grid[0, 0]), fig.add_subplot(grid[0, 1])
    farms = [row for row in vertices if row["Role"] != "hub"]
    positions = {"HUB": (3.85, 6.15)}
    for index, row in enumerate(farms):
        line, column = divmod(index, 8)
        if line % 2:
            column = 7 - column
        positions[row["Label"]] = (column * 1.1, 4.95 - line * 1.05)
    selected = next(row for row in priorities if row["RequestID"] == "R005")
    path = [label.strip() for label in selected["PathToHub"].strip("[]").split(",")]
    route_edges = {frozenset((path[index], path[index + 1])) for index in range(len(path) - 1)}
    cycle_edges = {frozenset(pair) for pair in (("a30b2", "c6748"), ("c6748", "c1c13"), ("c1c13", "a30b2"))}
    farm_index = {row["Label"]: index for index, row in enumerate(farms)}
    weights = {}
    for edge in edges:
        first, second = edge["Source"], edge["Destination"]
        pair = frozenset((first, second))
        weights[pair] = float(edge["TransportTime"])
        colour, width = "#AAAAAA", 1.0
        if pair in cycle_edges:
            colour, width = GREEN, 1.8
        if pair in route_edges:
            colour, width = ORANGE, 2.0
        curve = 0.0
        if "HUB" in pair:
            curve = 0.12 if second == "v75pu" else -0.15
        elif abs(farm_index[first] - farm_index[second]) == 2:
            curve = 0.27
        patch = FancyArrowPatch(positions[first], positions[second], arrowstyle="-",
                                shrinkA=14, shrinkB=14, linewidth=width, color=colour,
                                connectionstyle=f"arc3,rad={curve}", zorder=1)
        left.add_patch(patch)
    for row in vertices:
        label = row["Label"]
        x, y = positions[label]
        colour = ORANGE if row["Role"] == "hub" else PURPLE if row["Role"] == "isolated_farm" else BLUE
        left.text(x, y, label, ha="center", va="center", fontsize=8.6, zorder=3,
                  bbox={"boxstyle": "round,pad=0.27", "facecolor": "white", "edgecolor": colour,
                        "linewidth": 1.05})
    isolated = next(row["Label"] for row in vertices if row["Role"] == "isolated_farm")
    ix, iy = positions[isolated]
    left.annotate("isolated", (ix, iy), xytext=(ix, iy - 0.48), ha="center", fontsize=9, color=PURPLE)
    left.set(xlim=(-0.65, 8.3), ylim=(-0.40, 6.75))
    left.set_title(f"(a) Full schematic: {len(vertices)} vertices, {len(edges)} edges", pad=9)
    left.axis("off")
    legend = (Line2D((0,), (0,), color="#AAAAAA", lw=1.2, label="Other connection"),
              Line2D((0,), (0,), color=ORANGE, lw=2, label="R005 shortest route"),
              Line2D((0,), (0,), color=GREEN, lw=1.8, label="Detected cycle"))
    left.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, -0.09),
                frameon=False, ncol=3, fontsize=8.5, columnspacing=1.2)
    for index, label in enumerate(path):
        y = len(path) - 1 - index
        right.text(0.5, y, label, ha="center", va="center", fontsize=10.5,
                   bbox={"boxstyle": "round,pad=0.4", "facecolor": "white",
                         "edgecolor": ORANGE, "linewidth": 1.2})
        if index < len(path) - 1:
            weight = weights[frozenset((label, path[index + 1]))]
            arrow(right, (0.5, y - 0.20), (0.5, y - 0.8), colour=ORANGE)
            right.text(0.82, y - 0.5, f"{weight:.2f} min", fontsize=9.5, va="center")
    total = sum(weights[frozenset((path[index], path[index + 1]))] for index in range(len(path) - 1))
    if not math.isclose(total, float(selected["ShortestMinutes"]), abs_tol=1e-8):
        raise ValueError("Route edge sum differs from saved Dijkstra result")
    right.set(xlim=(-0.1, 1.6), ylim=(-0.75, len(path) - 0.25))
    right.set_title("(b) R005 route to HUB", pad=9)
    right.text(0.7, -0.6, f"Shortest total: {total:.2f} min", ha="center", fontsize=10)
    right.axis("off")
    fig.subplots_adjust(left=0.025, right=0.975, top=0.91, bottom=0.12)
    return fig


def bfsLevels(vertices, bfs):
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.set(xlim=(0, 10), ylim=(-0.5, 8.35))
    ax.axis("off")
    groups = {}
    for row in bfs:
        groups.setdefault(int(row["Level"]), []).append(row["Label"])
    for level in range(max(groups) + 1):
        y = 7.5 - level
        labels = groups[level]
        colour = ORANGE if level == 0 else BLUE
        ax.text(0.6, y, f"Level {level}", ha="left", va="center", fontweight="bold", fontsize=11)
        ax.add_patch(FancyBboxPatch((1.8, y - 0.37), 7.8, 0.74, boxstyle="round,pad=0.06",
                                    facecolor="white", edgecolor=colour, linewidth=0.8))
        rows = ["   ".join(labels[index:index + 8]) for index in range(0, len(labels), 8)]
        ax.text(2.02, y, "\n".join(rows), va="center", fontsize=10.2, fontfamily="DejaVu Sans Mono")
    isolated = [row["Label"] for row in vertices if row["Label"] not in {item["Label"] for item in bfs}]
    ax.text(0.6, 0.25, "Unreachable", ha="left", va="center", fontsize=11, color=PURPLE)
    ax.add_patch(FancyBboxPatch((1.8, -0.08), 7.8, 0.66, boxstyle="round,pad=0.06",
                                facecolor="white", edgecolor=PURPLE, linestyle="--", linewidth=1.0))
    ax.text(2.02, 0.25, ", ".join(isolated) + "  (isolated in the model)", va="center", fontsize=10.5)
    ax.text(5, 8.17, "BFS from HUB: minimum number of connections", ha="center", fontsize=12, fontweight="bold")
    fig.tight_layout(pad=0.5)
    return fig


def hashBehaviour():
    log = (ROOT / "sample_output/hash_tests.txt").read_text()
    example = log.split("=== EXPLICIT REAL-ID COLLISION AND TOMBSTONE ===", 1)[1]
    match = re.search(r"Both (\w+) and (\w+) hash to (\d+)", example)
    first, second, start_text = match.groups()
    start = int(start_text)
    found = re.search(rf"INSERT {second}: index=(\d+), count=2, size=(\d+)", example)
    destination, capacity = map(int, found.groups())
    checkpoints = []
    for count in (10, 20, 30, 37, 38, 40):
        match = re.search(rf"INSERT \w+: index=\d+, count={count}, size=(\d+), load=", log)
        if not match:
            raise ValueError("Missing required insertion state in hash trace")
        size = int(match.group(1))
        checkpoints.append((count, size, count / size))
    fig = plt.figure(figsize=(9.2, 4.2))
    grid = fig.add_gridspec(1, 2, width_ratios=(1.15, 1), wspace=0.3)
    left, right = fig.add_subplot(grid[0, 0]), fig.add_subplot(grid[0, 1])
    left.axis("off")
    left.set(xlim=(0, 4.4), ylim=(-0.85, 3.35))
    headers = ("Both inserted", "Delete qlctx", "Search c1c13")
    for column, header in enumerate(headers):
        x = 0.6 + column * 1.25
        left.text(x + 0.48, 2.65, header, ha="center", fontsize=9.5, fontweight="bold")
        for line, slot in enumerate((start, destination)):
            y = 1.75 - line * 0.82
            value = first if slot == start else second
            colour = BLUE if slot == start else GREEN
            if column > 0 and slot == start:
                value, colour = "DELETED", ORANGE
            left.add_patch(Rectangle((x, y), 0.98, 0.6, facecolor="white", edgecolor=colour, linewidth=1.0))
            left.text(x + 0.49, y + 0.3, value, ha="center", va="center", fontsize=9.5, color=colour)
            if column == 0:
                left.text(x - 0.15, y + 0.3, str(slot), va="center", ha="right", fontsize=10)
    arrow(left, (3.92, 2.05), (3.92, 1.24), colour=GREEN)
    left.text(2.2, 0.38, f"Probe order: {start} → {destination}; pass the tombstone", ha="center", fontsize=10)
    left.text(2.2, -0.11, f"Reinsert {first}: reuse tombstone at {start}", ha="center", fontsize=10)
    left.set_title(f"(a) Selected slots: double hashing, m = {capacity}", pad=12)
    x = [row[0] for row in checkpoints]
    loads = [row[2] for row in checkpoints]
    right.plot(x, loads, color=BLUE, linewidth=1.5, marker="s", markersize=5, markerfacecolor="white")
    right.axhline(0.7, color=GREY, linestyle="--", linewidth=0.9)
    right.text(10.2, 0.715, "Growth threshold 0.7", fontsize=9, color=GREY)
    right.annotate("53 → 107 slots\nbefore insert 38", xy=(38, 38 / 107), xytext=(24.5, 0.22),
                   fontsize=9.5, arrowprops={"arrowstyle": "->", "color": ORANGE}, color=ORANGE)
    for count, size, load in checkpoints:
        if count in (10, 20, 30, 40):
            right.annotate(f"{count}/{size}", (count, load), xytext=(0, 8), textcoords="offset points",
                           ha="center", fontsize=8.8)
    right.set(xlabel="Successful insertions", ylabel="Live records / table capacity",
              ylim=(0, 0.82), xlim=(8, 42), xticks=(10, 20, 30, 40))
    right.set_title("(b) Load factor and resizing", pad=12)
    setupChart(right)
    fig.subplots_adjust(left=0.025, right=0.975, top=0.85, bottom=0.18)
    return fig


def heapTree(states):
    row = next(item for item in states if item["Operation"] == "insertion" and item["OperationNumber"] == "12")
    entries = []
    for token in row["HeapArrayIndexOrder"].strip("[]").split(", "):
        request, priority = token.split(":")
        entries.append((request, float(priority)))
    for index in range(1, len(entries)):
        if entries[index][1] > entries[(index - 1) // 2][1]:
            raise ValueError("Saved heap state violates max-heap order")
    fig, ax = plt.subplots(figsize=(8.2, 4.15))
    depth = int(math.log2(len(entries)))
    positions = []
    for index in range(len(entries)):
        level = int(math.log2(index + 1))
        offset = index - (2 ** level - 1)
        positions.append(((offset + 0.5) * 8 / 2 ** level, depth - level))
    for index in range(1, len(entries)):
        ax.plot((positions[(index - 1) // 2][0], positions[index][0]),
                (positions[(index - 1) // 2][1], positions[index][1]), color=LIGHT, linewidth=1.2)
    for index, (request, priority) in enumerate(entries):
        x, y = positions[index]
        colour = ORANGE if index == 0 else BLUE
        ax.text(x, y, f"{request}\n{priority:.6f}", ha="center", va="center", fontsize=9,
                bbox={"boxstyle": "round,pad=0.32", "facecolor": "white", "edgecolor": colour,
                      "linewidth": 1.1}, zorder=3)
        ax.text(x, y + 0.37, f"i={index}", ha="center", fontsize=8, color=GREY)
    ax.set(xlim=(-0.15, 8.15), ylim=(-0.65, depth + 0.78))
    ax.axis("off")
    ax.text(4, depth + 0.68, "Max heap after 12 accepted insertions", ha="center", fontsize=12, fontweight="bold")
    ax.text(4, -0.57, "Labels: RequestID and P = F/T. Children of index i: 2i + 1 and 2i + 2.",
            ha="center", fontsize=9.5)
    fig.tight_layout(pad=0.5)
    return fig


def collectionOrder(priorities):
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    labels = [f"{row['CollectionOrder']}. {row['RequestID']}" for row in priorities]
    values = [float(row["Priority"]) for row in priorities]
    if any(values[index] > values[index - 1] for index in range(1, len(values))):
        raise ValueError("Saved collection order is not descending by priority")
    positions = list(range(len(values)))
    colours = [ORANGE if index < 5 else BLUE for index in positions]
    ax.barh(positions, values, color=colours, height=0.65, alpha=0.92)
    ax.set(yticks=positions, yticklabels=labels, xlabel="Calculated priority P = F/T (model tonnes/minute)",
           xlim=(0, max(values) * 1.24))
    for index, value in enumerate(values):
        ax.text(value + max(values) * 0.015, index, f"{value:.6f}", va="center", fontsize=9)
    ax.invert_yaxis()
    setupChart(ax)
    ax.grid(False, axis="y")
    ax.set_title("Collection order for the 12 accepted requests", pad=12)
    ax.legend(handles=(Line2D((0,), (0,), color=ORANGE, lw=6, label="First five extractions"),
                       Line2D((0,), (0,), color=BLUE, lw=6, label="Remaining requests")),
              frameon=False, loc="lower right")
    fig.tight_layout(pad=0.8)
    return fig


def sortingTimings(timings):
    fig, axes = plt.subplots(1, 3, figsize=(8.8, 3.2), sharey=True)
    conditions = (("random", "(a) Random"), ("nearly_sorted", "(b) Nearly sorted (10% moved)"),
                  ("reversed", "(c) Reversed"))
    for ax, (condition, title) in zip(axes, conditions):
        for name, colour, marker in (("Merge Sort", BLUE, "s"), ("Quick Sort", ORANGE, "o")):
            rows = [row for row in timings if row["Condition"] == condition and row["Algorithm"] == name]
            if tuple(int(row["Records"]) for row in rows) != (100, 500, 1000):
                raise ValueError("Timing matrix is incomplete or not in expected size order")
            ax.plot([int(row["Records"]) for row in rows],
                    [float(row["MeanMilliseconds"]) for row in rows],
                    label=name, color=colour, marker=marker, markersize=5,
                    markerfacecolor="white", linewidth=1.4)
        setupChart(ax)
        ax.set(title=title, xlabel="Collection records", xticks=(100, 500, 1000), xlim=(60, 1040))
        ax.set_ylim(bottom=0)
    axes[0].set_ylabel("Mean sorting time (ms)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=2, frameon=False, loc="lower center", bbox_to_anchor=(0.5, -0.01))
    fig.subplots_adjust(left=0.075, right=0.985, top=0.88, bottom=0.24, wspace=0.15)
    return fig


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    vertices = readCSV("report/figure_data/graph_vertices.csv")
    edges = readCSV("data/transport_edges.csv")
    bfs = readCSV("report/figure_data/bfs_levels.csv")
    priorities = readCSV("report/figure_data/priorities_and_collection_order.csv")
    states = readCSV("report/figure_data/heap_states.csv")
    timings = readCSV("sample_output/benchmark_results.csv")
    if len(vertices) != 41 or len(edges) != 55 or len(bfs) != 40 or len(priorities) != 12 or len(timings) != 18:
        raise ValueError("Figure inputs differ from the checked assignment dataset; refresh and review evidence")
    figures = (("01_system_uml", systemUML()), ("02_module_data_flow", moduleFlow()),
               ("03_farm_network", farmNetwork(vertices, edges, priorities)),
               ("04_bfs_levels", bfsLevels(vertices, bfs)), ("05_hash_behaviour", hashBehaviour()),
               ("06_max_heap", heapTree(states)), ("07_collection_order", collectionOrder(priorities)),
               ("08_sorting_timings", sortingTimings(timings)))
    with PdfPages(OUTPUT / "all_figures_preview.pdf") as preview:
        for filename, figure in figures:
            figure.savefig(OUTPUT / (filename + ".pdf"), bbox_inches="tight", pad_inches=0.12)
            figure.savefig(OUTPUT / (filename + ".png"), bbox_inches="tight", pad_inches=0.12)
            preview.savefig(figure, bbox_inches="tight", pad_inches=0.12)
            plt.close(figure)
            print("Created", filename + ".pdf and .png")
    inputs = ("report/figure_data/graph_vertices.csv", "data/transport_edges.csv",
              "report/figure_data/bfs_levels.csv", "report/figure_data/priorities_and_collection_order.csv",
              "report/figure_data/heap_states.csv", "sample_output/hash_tests.txt",
              "sample_output/benchmark_results.csv", "sample_output/benchmark_environment.json")
    manifest = {"palette_reference": "Containement_Not_Recovery (1).pdf",
                "palette_method": "RGB drawing operators extracted from the supplied reference PDF",
                "palette": {"blue": BLUE, "orange": ORANGE, "green": GREEN, "purple": PURPLE},
                "matplotlib_version": matplotlib.__version__, "png_dpi": 300,
                "font": "STIXGeneral; DejaVu Sans Mono for BFS IDs", "error_bars": False,
                "figures": [name for name, _ in figures],
                "input_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in inputs}}
    (OUTPUT / "figures_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
