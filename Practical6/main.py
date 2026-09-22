from DSAGraph import DSAGraph


def display_menu():
    print("\n========================================")
    print("           GRAPH EXPLORER MENU")
    print("========================================")
    print("1. Add Node (Vertex)")
    print("2. Delete Node (Vertex)")
    print("3. Add Edge")
    print("4. Delete Edge")
    print("5. Display as Adjacency List")
    print("6. Display as Adjacency Matrix")
    print("7. Breadth First Search (BFS)")
    print("8. Depth First Search (DFS)")
    print("9. Load Sample Graph 1 (Activity 2)")
    print("10. Load Sample Graph 2 (Activity 2)")
    print("0. Exit")
    print("========================================")


def format_search_edges(queue_of_edges):
    result = ""
    source_label = None
    is_first = True

    for item in queue_of_edges:
        if source_label is None:
            source_label = item
        else:
            if not is_first:
                result += ", "
            result += "(" + str(source_label) + " -> " + str(item) + ")"
            source_label = None
            is_first = False

    return result


def load_graph_one(graph):
    graph.addEdge("A", "B")
    graph.addEdge("A", "C")
    graph.addEdge("A", "D")
    graph.addEdge("B", "E")
    graph.addEdge("C", "D")
    graph.addEdge("D", "F")
    graph.addEdge("E", "F")
    graph.addEdge("E", "G")
    graph.addEdge("F", "G")
    print("Sample Graph 1 loaded successfully (7 vertices, 9 edges).")


def load_graph_two(graph):
    graph.addEdge("A", "B")
    graph.addEdge("A", "C")
    graph.addEdge("A", "D")
    graph.addEdge("B", "E")
    graph.addEdge("C", "F")
    graph.addEdge("D", "E")
    graph.addEdge("D", "F")
    graph.addEdge("D", "H")
    graph.addEdge("E", "G")
    graph.addEdge("F", "I")
    graph.addEdge("G", "H")
    graph.addEdge("G", "J")
    graph.addEdge("H", "I")
    graph.addEdge("H", "J")
    graph.addEdge("I", "J")
    print("Sample Graph 2 loaded successfully (10 vertices, 15 edges).")


def main():
    graph = DSAGraph()
    running = True

    while running:
        display_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            label = input("Enter node label: ").strip()
            try:
                graph.addVertex(label)
                print("Node added:", label)
            except ValueError as error:
                print("Error:", error)

        elif choice == "2":
            label = input("Enter node label to delete: ").strip()
            try:
                graph.deleteVertex(label)
                print("Node deleted:", label)
            except KeyError as error:
                print("Error:", error)

        elif choice == "3":
            source_label = input("Enter first node label: ").strip()
            destination_label = input("Enter second node label: ").strip()
            try:
                graph.addEdge(source_label, destination_label)
                print("Edge added between", source_label, "and", destination_label)
            except Exception as error:
                print("Error:", error)

        elif choice == "4":
            source_label = input("Enter first node label: ").strip()
            destination_label = input("Enter second node label: ").strip()
            try:
                graph.deleteEdge(source_label, destination_label)
                print("Edge deleted between", source_label, "and", destination_label)
            except KeyError as error:
                print("Error:", error)

        elif choice == "5":
            if graph.isEmpty():
                print("Graph is currently empty.")
            else:
                print("\n--- Adjacency List ---")
                print(graph.displayAsList())

        elif choice == "6":
            if graph.isEmpty():
                print("Graph is currently empty.")
            else:
                print("\n--- Adjacency Matrix ---")
                print(graph.displayAsMatrix())

        elif choice == "7":
            if graph.isEmpty():
                print("Graph is currently empty.")
            else:
                start_label = input("Enter starting node (or press Enter for default): ").strip()
                if start_label == "":
                    start_label = None
                try:
                    bfs_edges = graph.breadthFirstSearch(start_label)
                    print("\nBFS Spanning Tree Edges:")
                    print(format_search_edges(bfs_edges))
                except (KeyError, ValueError) as error:
                    print("Error:", error)

        elif choice == "8":
            if graph.isEmpty():
                print("Graph is currently empty.")
            else:
                start_label = input("Enter starting node (or press Enter for default): ").strip()
                if start_label == "":
                    start_label = None
                try:
                    dfs_edges = graph.depthFirstSearch(start_label)
                    print("\nDFS Spanning Tree Edges:")
                    print(format_search_edges(dfs_edges))
                except (KeyError, ValueError) as error:
                    print("Error:", error)

        elif choice == "9":
            graph = DSAGraph()
            load_graph_one(graph)

        elif choice == "10":
            graph = DSAGraph()
            load_graph_two(graph)

        elif choice == "0":
            print("Exiting graph explorer...")
            running = False

        else:
            print("Invalid choice, please select a valid option from the menu.")


if __name__ == "__main__":
    main()
