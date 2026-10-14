"""Check normal CSV input failures and the menu's recovery/exit behavior."""

import csv
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from DataLoader import ROOT, buildSystem, loadFarmRecords, loadGraph, loadRequests
from TestHelpers import check, expectError


def runTests():
    records, _, _, scheduler = buildSystem()
    with tempfile.TemporaryDirectory(prefix="comp5008_input_") as directory:
        temporary = Path(directory)
        path = temporary / "bad.csv"
        path.write_text("Id,Name\nabc,Example\n")
        expectError("missing farm headers", ValueError, lambda: loadFarmRecords(path))
        path.write_text("")
        expectError("empty farm CSV", ValueError, lambda: loadFarmRecords(path))
        expectError("missing farm file", FileNotFoundError,
                    lambda: loadFarmRecords(temporary / "missing.csv"))
        with (ROOT / "data/dataset.csv").open(newline="", encoding="utf-8") as source:
            reader = csv.reader(source)
            headers = next(reader)
            row = next(reader)
        with path.open("w", newline="") as target:
            writer = csv.writer(target)
            writer.writerow(headers)
            writer.writerow(row[:5])
        expectError("truncated farm row", ValueError, lambda: loadFarmRecords(path))
        row[headers.index("Lat")] = "not-a-number"
        with path.open("w", newline="") as target:
            writer = csv.writer(target)
            writer.writerow(headers)
            writer.writerow(row)
        expectError("invalid coordinate in farm CSV", ValueError, lambda: loadFarmRecords(path))
        path.write_text("Source,Destination\nHUB,bad\n")
        expectError("missing edge headers", ValueError, lambda: loadGraph(records, path))
        path.write_text("Source,Destination,TransportTime\nHUB,MISSING,1\n")
        expectError("invalid edge endpoint in CSV", ValueError, lambda: loadGraph(records, path))
        path.write_text("RequestID,FarmID\nR1,bad\n")
        expectError("missing request headers", ValueError, lambda: loadRequests(scheduler, path))
        # A malformed row is rejected, then a subsequent valid row still loads.
        path.write_text("RequestID,FarmID,EstimatedFeedstock\nBAD\nGOOD,"
                        + records.peekFirst().farm_id + ",10\n")
        accepted, rejected = loadRequests(scheduler, path)
        check("request loader continues after truncated row", accepted == 1 and rejected == 1)

        # Isolate menu operations that write benchmark/CSV output from saved evidence.
        package = temporary / "package"
        shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns(
            "__pycache__", ".DS_Store", "sample_output", "report"))
        new_farm = ("6\nnew01\nTest new farm\nPigs\n-32\n116\n\nTest Road\n"
                    "Test Town\nWA\n6000\nAustralia\n")
        session = (new_farm + "15\n16\nnew01\n17\nHUB\nnew01\n10\n"
                   "1\n2\nHUB\n3\nHUB\n4\nnew01\nHUB\n5\nnew01\n"
                   "8\n9\nNEWREQUEST\nnew01\n20\n10\n12\n11\n13\n"
                   "14\n1\n14\n2\n7\nnew01\n0\n")
        process = subprocess.run([sys.executable, str(package / "main.py")],
                                 input=session, text=True, cwd=directory,
                                 capture_output=True, timeout=20)
        check("all menu options work from an isolated extracted package",
              process.returncode == 0 and not process.stderr
              and "Error:" not in process.stdout and "1000 reversed" in process.stdout
              and "Undirected connection added." in process.stdout
              and "COLLECT: NEWREQUEST" in process.stdout
              and "Accepted=12, rejected=7" in process.stdout)
        exported = package / "sample_output/collection_records_sorted.csv"
        with exported.open(newline="", encoding="utf-8") as source:
            saved = tuple(csv.DictReader(source))
        check("menu exports complete sorted accepted history", len(saved) == 13
              and all(float(saved[index - 1]["TransportTime"]) <= float(saved[index]["TransportTime"])
                      for index in range(1, len(saved))))

        # A CSV parser failure can happen before normal per-row validation.
        (package / "data/collection_requests.csv").write_text(
            "RequestID,FarmID,EstimatedFeedstock\n" + "X" * (csv.field_size_limit() + 1)
            + "," + records.peekFirst().farm_id + ",10\n")
        process = subprocess.run([sys.executable, str(package / "main.py")],
                                 input="13\n0\n", text=True, cwd=directory,
                                 capture_output=True, timeout=20)
        check("CSV parser errors are handled and menu continues",
              process.returncode == 0 and not process.stderr
              and "Error: field larger than field limit" in process.stdout
              and "Exiting..." in process.stdout)

    # Run from a different working directory to verify file path handling.
    process = subprocess.run([sys.executable, str(ROOT / "main.py")],
                             input="invalid\n5\nzzzzz\n10\n11\n0\n", text=True,
                             cwd=tempfile.gettempdir(), capture_output=True, timeout=20)
    check("menu rejects input and continues", process.returncode == 0
          and "Invalid menu option" in process.stdout and "Farm not found" in process.stdout
          and "Heap is empty" in process.stdout and "Exiting..." in process.stdout
          and "Traceback" not in process.stderr)
    process = subprocess.run([sys.executable, str(ROOT / "main.py")], input="", text=True,
                             cwd=tempfile.gettempdir(), capture_output=True, timeout=20)
    check("menu EOF cleanly exits", process.returncode == 0 and "Exiting..." in process.stdout
          and "Traceback" not in process.stderr)
    print("INPUT AND MENU TESTS PASSED")


if __name__ == "__main__":
    runTests()
