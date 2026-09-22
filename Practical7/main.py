from DSAHashTable import DSAHashTable


def main():
    small_table = DSAHashTable(5)
    small_table.put("A", "Apple")
    small_table.put("F", "Fish")
    small_table.put("K", "Kiwi")

    print("Small table after inserting three keys:")
    print(small_table)
    print("Has F:", small_table.hasKey("F"))
    print("Value for F:", small_table.get("F"))

    small_table.remove("F")
    small_table.put("P", "Pear")
    print("Small table after remove and insert:")
    print(small_table)

    data_table = DSAHashTable(11)
    data_table.load("RandomNames7000(1).csv")
    print("CSV records stored:", data_table.getCount())
    print("Current table size:", data_table.getSize())
    print("Current load factor:", data_table.loadFactor())
    print("Name for 14495655:", data_table.get("14495655"))

    data_table.save("RandomNames7000_saved.csv")

    reloaded_table = DSAHashTable(11)
    reloaded_table.load("RandomNames7000_saved.csv")
    print("Reloaded records:", reloaded_table.getCount())


if __name__ == "__main__":
    main()
