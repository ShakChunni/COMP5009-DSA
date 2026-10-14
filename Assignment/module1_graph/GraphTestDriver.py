import math
from DataLoader import buildSystem, HUB
from module1_graph.DSAGraph import DSAGraph
from TestHelpers import check, expectError


def runTests():
    records, _, graph, _ = buildSystem()
    print("=== REQUIRED DATASET GRAPH ===")
    print("Vertices:", graph.getVertexCount(), "Edges:", graph.getEdgeCount())
    print(graph.displayAsList())
    print("BFS from HUB:")
    print(graph.displayBFS(HUB))
    order, cycle = graph.depthFirstSearch(HUB)
    print("DFS visit order (all components):", order)
    print("Cycle exists:", not cycle.isEmpty(), "Detected cycle:", cycle)
    check("required graph size", graph.getVertexCount() >= 10 and graph.getEdgeCount() >= 12)
    check("dataset graph contains a cycle", not cycle.isEmpty())
    check("DFS includes every component", order.count() == graph.getVertexCount())
    isolated = records.peekLast().farm_id
    check("deliberately isolated farm", graph.getVertex(isolated).adjacent.isEmpty())
    minutes, path = graph.dijkstra(records.peekFirst().farm_id, HUB)
    print(f"Dijkstra farm -> hub: path={path}, shortest time={minutes:.2f} min")
    minutes, path = graph.dijkstra(HUB, isolated)
    print(f"Unreachable {isolated}: no valid route (time={minutes}, path={path})")
    check("unreachable destination", math.isinf(minutes) and path.isEmpty())
    check("BFS excludes isolated farm", graph.breadthFirstSearch(HUB).count() == 40)
    for vertex in graph.vertices():
        for edge in vertex.adjacent:
            reverse_weight = None
            for reverse in edge.destination.adjacent:
                if reverse.destination is vertex:
                    reverse_weight = reverse.weight
            check(f"undirected positive edge {vertex.label}->{edge.destination.label}",
                  reverse_weight == edge.weight and edge.weight > 0)

    print("=== SMALL INDEPENDENT GRAPH FIXTURE ===")
    small = DSAGraph()
    for label in ("A", "B", "C", "D", "E", "Z"):
        small.addVertex(label)
    for first, second, weight in (("A", "B", 4), ("A", "C", 1), ("C", "B", 2),
                                  ("B", "D", 1), ("C", "D", 5), ("D", "E", 3)):
        small.addEdge(first, second, weight)
    time, path = small.dijkstra("A", "E")
    print("Known shortest path:", path, "time:", time)
    check("Dijkstra beats direct expensive edges", time == 7 and str(path) == "[A, C, B, D, E]")
    check("BFS grouped levels", small.displayBFS("A") == "Level 0: A\nLevel 1: B, C\nLevel 2: D\nLevel 3: E")
    time, path = small.dijkstra("A", "A")
    check("same source and destination", time == 0 and str(path) == "[A]")
    check("isolated BFS", small.displayBFS("Z") == "Level 0: Z")
    expectError("duplicate location", ValueError, lambda: small.addVertex("A"))
    expectError("duplicate reversed edge", ValueError, lambda: small.addEdge("B", "A", 3))
    expectError("self-edge", ValueError, lambda: small.addEdge("A", "A", 2))
    expectError("unknown vertex", KeyError, lambda: small.addEdge("A", "MISSING", 2))
    expectError("empty vertex label", ValueError, lambda: small.addVertex(" "))
    expectError("invalid BFS source", KeyError, lambda: small.breadthFirstSearch("MISSING"))
    expectError("invalid DFS source", KeyError, lambda: small.depthFirstSearch("MISSING"))
    expectError("invalid Dijkstra destination", KeyError, lambda: small.dijkstra("A", "MISSING"))
    for value in (0, -1, "bad", float("nan"), float("inf"), True, None):
        expectError(f"invalid edge weight {value}", ValueError,
                    lambda value=value: small.addEdge("A", "Z", value))
    expectError("empty graph source", KeyError, lambda: DSAGraph().dijkstra("A", "B"))
    expectError("oversized integer weight", ValueError, lambda: small.addEdge("A", "Z", 10 ** 1000))

    huge = DSAGraph()
    for label in ("A", "B", "C"):
        huge.addVertex(label)
    huge.addEdge("A", "B", 1e308)
    huge.addEdge("B", "C", 1e308)
    expectError("overflowing path total is not reported as unreachable", ValueError,
                lambda: huge.dijkstra("A", "C"))
    alternate = DSAGraph()
    for label in ("A", "B", "C", "D", "T", "Z"):
        alternate.addVertex(label)
    for first, second, weight in (("A", "B", 1e308), ("B", "D", 1e308),
                                  ("A", "C", 1), ("C", "T", 1.1e308)):
        alternate.addEdge(first, second, weight)
    check("irrelevant overflow does not hide finite shortest route",
          alternate.dijkstra("A", "T")[0] == 1.1e308)
    check("unreachable stays unreachable despite overflow elsewhere",
          math.isinf(alternate.dijkstra("A", "Z")[0]))

    tree = DSAGraph()
    for label in ("A", "B", "Z", "F", "G", "H"):
        tree.addVertex(label)
    tree.addEdge("A", "B", 1)
    _, cycle = tree.depthFirstSearch("A")
    check("tree parent edge is not a cycle", cycle.isEmpty())
    tree.addEdge("F", "G", 1)
    tree.addEdge("G", "H", 1)
    tree.addEdge("H", "F", 1)
    _, cycle = tree.depthFirstSearch("A")
    print("Cycle in disconnected component:", cycle)
    check("disconnected component cycle detected", str(cycle) == "[F, G, H, F]")
    long_path = DSAGraph()
    for index in range(1100):
        long_path.addVertex(f"V{index}")
        if index > 0:
            long_path.addEdge(f"V{index - 1}", f"V{index}", 1)
    order, cycle = long_path.depthFirstSearch("V0")
    check("iterative DFS handles 1100-vertex path", order.count() == 1100 and cycle.isEmpty())
    print("GRAPH TESTS PASSED")


if __name__ == "__main__":
    runTests()
