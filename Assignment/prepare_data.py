"""Reproduce the selected dataset and educational network from the supplied CSV."""

import csv
import math
from DataLoader import ROOT, HUB

HUB_LAT = -32.23
HUB_LNG = 115.78


def estimatedMinutes(first_lat, first_lng, second_lat, second_lng):
    """Great-circle distance * 1.3 road factor / 60 km/h, expressed in minutes."""
    lat1, lat2 = math.radians(float(first_lat)), math.radians(float(second_lat))
    difference_lat = lat2 - lat1
    difference_lng = math.radians(float(second_lng) - float(first_lng))
    value = (math.sin(difference_lat / 2) ** 2
             + math.cos(lat1) * math.cos(lat2) * math.sin(difference_lng / 2) ** 2)
    # Clamp rounding error before square roots near antipodal coordinates.
    value = min(1.0, max(0.0, value))
    distance = 6371.0 * 2 * math.atan2(math.sqrt(value), math.sqrt(1 - value))
    return max(1.0, round(distance * 1.3, 2))


def main():
    source_path = ROOT / "farm_dataset_sample.csv"
    selected = [None] * 40
    count = 0
    with source_path.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fieldnames = reader.fieldnames
        for row in reader:
            eligible = (row["State"] == "WA" and row["Last Known Status"] == "Open"
                        and "unconfirmed" not in row["Categories"].lower()
                        and "unconfirmed" not in row["Species"].lower()
                        and "proposed" not in row["Name"].lower()
                        and any(species in row["Species"].split(", ")
                                for species in ("Cows/cattle", "Pigs", "Sheep", "Goats")))
            if eligible and count < 40:
                selected[count] = row
                count += 1
    if count < 40:
        raise ValueError("Source does not contain 40 eligible WA records")
    (ROOT / "data").mkdir(exist_ok=True)
    with (ROOT / "data/dataset.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        for row in selected:
            writer.writerow(row)

    with (ROOT / "data/transport_edges.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(("Source", "Destination", "TransportTime"))

        def connect(first_index, second_index):
            first = selected[first_index] if first_index >= 0 else None
            second = selected[second_index]
            minutes = estimatedMinutes(first["Lat"] if first else HUB_LAT,
                                       first["Lng"] if first else HUB_LNG,
                                       second["Lat"], second["Lng"])
            writer.writerow((first["Id"] if first else HUB, second["Id"], minutes))

        connect(-1, 0)
        for index in range(38):
            connect(index, index + 1)
        for index in (10, 20, 30):
            connect(-1, index)
        for index in range(0, 37, 3):
            connect(index, index + 2)
        # selected[39] is deliberately isolated for the required unreachable test.

    with (ROOT / "data/collection_requests.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target)
        writer.writerow(("RequestID", "FarmID", "EstimatedFeedstock"))
        for index in range(12):
            writer.writerow((f"R{index + 1:03}", selected[index]["Id"], 10 + (index * 7) % 31))
        # Intentional invalid rows demonstrate validation; these are not farm data.
        writer.writerow(("R001", selected[12]["Id"], 20))
        writer.writerow(("DUPFARM", selected[0]["Id"], 20))
        writer.writerow(("ISOLATED", selected[39]["Id"], 20))
        writer.writerow(("MISSING", "zzzzz", 20))
        writer.writerow(("BADID", "", 20))
        writer.writerow(("NEGATIVE", selected[13]["Id"], -1))
        writer.writerow(("NOTFINITE", selected[14]["Id"], "nan"))
    print("Prepared 40 farms, 41 vertices, 55 edges, 12 valid and 7 invalid requests.")


if __name__ == "__main__":
    main()
