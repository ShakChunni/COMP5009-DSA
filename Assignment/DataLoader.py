import csv
from pathlib import Path
from common.DSALinkedList import DSALinkedList
from FarmRecord import FarmRecord
from module1_graph.DSAGraph import DSAGraph
from module2_hash.DSAHashTable import DSAHashTable
from CollectionScheduler import CollectionScheduler

ROOT = Path(__file__).resolve().parent
HUB = "HUB"


def loadFarmRecords(filename):
    """CSV parsing only; the hash table, not DictReader, performs farm lookup."""
    records = DSALinkedList()
    required = ("Id", "Name", "Species", "Lat", "Lng", "Street Num", "Street",
                "Suburb", "State", "Postcode", "Country")
    with open(filename, newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or any(field not in reader.fieldnames for field in required):
            raise ValueError("Farm CSV is missing required column headers")
        for row in reader:
            try:
                if any(row[field] is None for field in required):
                    raise ValueError("Farm CSV row has missing columns")
                record = FarmRecord(row["Id"], row["Name"], row["Species"],
                                    row["Lat"], row["Lng"], row["Street Num"],
                                    row["Street"], row["Suburb"], row["State"],
                                    row["Postcode"], row["Country"],
                                    row.get("Map URL", ""), row.get("Profile URL", ""),
                                    row.get("Last Known Status", ""))
            except (ValueError, TypeError) as error:
                raise ValueError(f"Farm CSV line {reader.line_num}: {error}") from error
            records.insertLast(record)
    return records


def loadGraph(records, edge_filename):
    graph = DSAGraph()
    graph.addVertex(HUB, "Proposed Kwinana-area biogas hub")
    for record in records:
        graph.addVertex(record.farm_id, record.name)
    with open(edge_filename, newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        required = ("Source", "Destination", "TransportTime")
        if reader.fieldnames is None or any(field not in reader.fieldnames for field in required):
            raise ValueError("Edge CSV is missing required headers")
        for row in reader:
            try:
                graph.addEdge(row["Source"], row["Destination"], row["TransportTime"])
            except (ValueError, TypeError, KeyError) as error:
                raise ValueError(f"Edge CSV line {reader.line_num}: {error}") from error
    return graph


def buildSystem(trace=False):
    records = loadFarmRecords(ROOT / "data/dataset.csv")
    farms = DSAHashTable(53)
    for record in records:
        farms.insert(record, trace=trace)
    graph = loadGraph(records, ROOT / "data/transport_edges.csv")
    scheduler = CollectionScheduler(farms, graph, HUB)
    return records, farms, graph, scheduler


def loadRequests(scheduler, filename):
    accepted = 0
    rejected = 0
    with open(filename, newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        required = ("RequestID", "FarmID", "EstimatedFeedstock")
        if reader.fieldnames is None or any(field not in reader.fieldnames for field in required):
            raise ValueError("Request CSV is missing required headers")
        for row in reader:
            try:
                scheduler.insert(row["RequestID"], row["FarmID"], row["EstimatedFeedstock"])
                accepted += 1
            except (ValueError, KeyError, TypeError) as error:
                print(f"REJECTED request CSV line {reader.line_num}: {error}")
                rejected += 1
    return accepted, rejected


def writeCollectionRecords(filename, records):
    with open(filename, "w", newline="", encoding="utf-8") as destination:
        writer = csv.writer(destination)
        writer.writerow(("RequestID", "FarmID", "EstimatedFeedstock", "TransportTime",
                         "Priority", "Status"))
        for request in records:
            writer.writerow((request.request_id, request.farm_id, request.feedstock,
                             request.transport_time, request.priority, request.status))
