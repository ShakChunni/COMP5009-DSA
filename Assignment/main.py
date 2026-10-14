import csv
from DataLoader import ROOT, HUB, buildSystem, loadRequests, writeCollectionRecords
from FarmRecord import FarmRecord
from module4_sorting.DSAsorts import mergeSort, quickSort
from module4_sorting.benchmark import runBenchmarks


def menu():
    print("\n=== BIOGAS FEEDSTOCK COLLECTION NETWORK ===")
    print("1. Display farm transport graph")
    print("2. BFS levels")
    print("3. DFS cycle detection")
    print("4. Shortest transportation route")
    print("5. Search farm by ID")
    print("6. Insert farm record")
    print("7. Delete farm record")
    print("8. Display hash table and load factor")
    print("9. Add collection request")
    print("10. Peek highest-priority request")
    print("11. Extract highest-priority request")
    print("12. Display pending heap")
    print("13. Load supplied request test data")
    print("14. Sort/export all accepted collection records")
    print("15. Run sorting benchmarks")
    print("16. Add graph location")
    print("17. Add weighted transport connection")
    print("0. Exit")


def inputFarm():
    return FarmRecord(input("FarmID (preserved exactly): "), input("Name: "), input("Species: "),
                      input("Latitude: "), input("Longitude: "), input("Street number: "),
                      input("Street: "), input("Suburb: "), input("State: "),
                      input("Postcode: "), input("Country: "))


def main():
    try:
        _, farms, graph, scheduler = buildSystem()
    except (OSError, ValueError, KeyError, csv.Error) as error:
        print("Cannot load system:", error)
        return
    print(f"Loaded {farms.getCount()} farms, {graph.getVertexCount()} locations, "
          f"{graph.getEdgeCount()} undirected edges. Hub={HUB}")
    running = True
    while running:
        try:
            menu()
            choice = input("Choose an option: ").strip()
            if choice == "1":
                print(graph.displayAsList())
            elif choice == "2":
                print(graph.displayBFS(input("Source location (HUB or FarmID): ").strip()))
            elif choice == "3":
                order, cycle = graph.depthFirstSearch(input("Source location: ").strip())
                print("DFS order (all components):", order)
                print("Cycle exists:", not cycle.isEmpty(), "Detected cycle:", cycle)
            elif choice == "4":
                source = input("Source: ").strip()
                destination = input("Destination: ").strip()
                minutes, path = graph.dijkstra(source, destination)
                if path.isEmpty():
                    print("Destination is unreachable; no valid transportation route.")
                else:
                    print("Shortest route:", path, f"Time: {minutes:.2f} minutes")
            elif choice == "5":
                print(farms.search(input("FarmID: "), trace=True))
            elif choice == "6":
                record = inputFarm()
                farms.insert(record, trace=True)
                print("Farm saved. Use option 16 to add its graph location and 17 to connect it.")
            elif choice == "7":
                farms.delete(input("FarmID: "), trace=True)
            elif choice == "8":
                farms.display()
                print(f"Count={farms.getCount()}, size={farms.getSize()}, load={farms.loadFactor():.4f}")
            elif choice == "9":
                scheduler.insert(input("Request ID: "), input("FarmID: "),
                                 input("Estimated feedstock (model tonnes): "))
            elif choice == "10":
                print("PEEK:", scheduler.peek())
            elif choice == "11":
                scheduler.extract_priority()
            elif choice == "12":
                print(scheduler.heap.arrayString())
            elif choice == "13":
                accepted, rejected = loadRequests(scheduler, ROOT / "data/collection_requests.csv")
                print(f"Accepted={accepted}, rejected={rejected}")
            elif choice == "14":
                records = [None] * scheduler.history.count()
                for index, request in enumerate(scheduler.history):
                    records[index] = request
                algorithm = input("Sort: 1=Merge Sort, 2=Quick Sort: ").strip()
                if algorithm == "1":
                    mergeSort(records)
                elif algorithm == "2":
                    quickSort(records)
                else:
                    raise ValueError("Choose 1 or 2")
                for request in records:
                    print(request, "Status=" + request.status)
                output = ROOT / "sample_output/collection_records_sorted.csv"
                output.parent.mkdir(exist_ok=True)
                writeCollectionRecords(output, records)
                print("Saved:", output)
            elif choice == "15":
                runBenchmarks(scheduler)
            elif choice == "16":
                farm_id = input("FarmID to add as a location: ")
                record = farms.search(farm_id)
                graph.addVertex(farm_id, record.name)
                print("Graph location added (isolated until connected).")
            elif choice == "17":
                graph.addEdge(input("Source location: ").strip(),
                              input("Destination location: ").strip(),
                              input("Transportation time in minutes: "))
                print("Undirected connection added.")
            elif choice == "0":
                running = False
                print("Exiting...")
            else:
                print("Invalid menu option")
        except (ValueError, KeyError, OSError, TypeError, csv.Error) as error:
            print("Error:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            running = False


if __name__ == "__main__":
    main()
