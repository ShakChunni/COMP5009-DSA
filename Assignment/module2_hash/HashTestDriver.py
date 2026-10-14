from DataLoader import ROOT, loadFarmRecords
from FarmRecord import FarmRecord
from module2_hash.DSAHashTable import DSAHashTable
from TestHelpers import check, expectError


def runTests():
    records = loadFarmRecords(ROOT / "data/dataset.csv")
    table = DSAHashTable(53)
    print("=== 40 REAL FARM INSERTIONS WITH PROBING AND RESIZING ===")
    for record in records:
        table.insert(record, trace=True)
    check("40 farm records loaded", table.getCount() == 40)
    check("resized to prime capacity 107", table.getSize() == 107)
    for record in records:
        check("complete record retrieved " + record.farm_id, table.search(record.farm_id) is record)
    print("Complete successful search:", table.search(records.peekFirst().farm_id, trace=True))
    expectError("missing farm search", KeyError, lambda: table.search("zzzzz", trace=True))
    expectError("duplicate FarmID", ValueError, lambda: table.insert(records.peekFirst(), trace=True))
    before = table.getCount()
    table.delete(records.peekFirst().farm_id, trace=True)
    check("deletion changes count/load", table.getCount() == before - 1 and table.loadFactor() == 39 / 107)
    expectError("search after deletion", KeyError, lambda: table.search(records.peekFirst().farm_id, trace=True))
    expectError("repeat deletion", KeyError, lambda: table.delete(records.peekFirst().farm_id, trace=True))
    expectError("missing deletion", KeyError, lambda: table.delete("zzzzz", trace=True))
    table.insert(records.peekFirst(), trace=True)
    check("reinsertion after deletion", table.search(records.peekFirst().farm_id) is records.peekFirst())

    print("=== EXPLICIT REAL-ID COLLISION AND TOMBSTONE ===")
    collision_table = DSAHashTable(53)
    first = second = None
    for candidate in records:
        for other in records:
            if candidate is not other and collision_table.hash(candidate.farm_id) == collision_table.hash(other.farm_id):
                first, second = candidate, other
                break
        if first is not None:
            break
    check("collision pair found in actual dataset", first is not None)
    print(f"Both {first.farm_id} and {second.farm_id} hash to {collision_table.hash(first.farm_id)}")
    collision_table.insert(first, trace=True)
    collision_table.insert(second, trace=True)
    collision_table.delete(first.farm_id, trace=True)
    check("search continues beyond tombstone", collision_table.search(second.farm_id, trace=True) is second)
    collision_table.insert(first, trace=True)
    check("tombstone reusable", collision_table.getCount() == 2)

    print("=== RECORD VALIDATION ===")
    valid = records.peekFirst()

    def makeRecord(farm_id=valid.farm_id, name=valid.name, lat=valid.latitude, lng=valid.longitude):
        return FarmRecord(farm_id, name, valid.species, lat, lng, valid.street_num,
                          valid.street, valid.suburb, valid.state, valid.postcode, valid.country)

    for identifier in ("", " bad", "bad-id", None, 123, "é123"):
        expectError(f"invalid FarmID {identifier}", ValueError, lambda identifier=identifier: makeRecord(farm_id=identifier))
        expectError("invalid search ID", ValueError, lambda identifier=identifier: table.search(identifier))
    expectError("blank farm name", ValueError, lambda: makeRecord(name=" "))
    for value in ("bad", None, True, float("nan"), float("inf"), 91, -91):
        expectError(f"invalid latitude {value}", ValueError, lambda value=value: makeRecord(lat=value))
    for value in ("bad", None, True, float("nan"), float("inf"), 181, -181):
        expectError(f"invalid longitude {value}", ValueError, lambda value=value: makeRecord(lng=value))
    check("coordinate boundary values accepted", makeRecord(lat=90, lng=-180).latitude == 90)
    expectError("oversized coordinate integer", ValueError, lambda: makeRecord(lat=10 ** 1000))
    expectError("invalid table record", ValueError, lambda: table.insert("not a record"))
    print("HASH TESTS PASSED")


if __name__ == "__main__":
    runTests()
