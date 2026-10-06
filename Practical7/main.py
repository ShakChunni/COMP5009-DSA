from DSAHashTable import DSAHashTable


def main():
    table = DSAHashTable(5)
    choice = ""

    while choice != "0":
        print("\n1. Add entry")
        print("2. Display table")
        print("3. Find entry")
        print("4. Remove entry")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            key = input("Enter key: ")
            value = input("Enter value: ")
            table.put(key, value)
            print("Entry added or updated.")
        elif choice == "2":
            print(table)
        elif choice == "3":
            key = input("Enter key: ")
            if table.hasKey(key):
                print("Value:", table.get(key))
            else:
                print("Key not found")
        elif choice == "4":
            key = input("Enter key: ")
            if table.hasKey(key):
                table.remove(key)
                print("Entry removed.")
            else:
                print("Key not found")
        elif choice != "0":
            print("Invalid option")


if __name__ == "__main__":
    main()
