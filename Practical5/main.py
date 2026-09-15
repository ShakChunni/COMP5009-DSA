from DSABinarySearchTree import DSABinarySearchTree


def display_menu():
    print("\n========================================")
    print("     BINARY SEARCH TREE MENU")
    print("========================================")
    print("1. Add Node (Insert)")
    print("2. Delete Node")
    print("3. Find Node")
    print("4. Display Tree (Traversals)")
    print("5. Tree Height")
    print("6. Min & Max Keys")
    print("7. Tree Balance Score")
    print("8. Load Sample Tree")
    print("0. Exit")
    print("========================================")


def display_traversal_menu():
    print("\n--- Choose Traversal Type ---")
    print("1. In-order")
    print("2. Pre-order")
    print("3. Post-order")
    print("0. Cancel")


def handle_traversals(tree):
    if tree.isEmpty():
        print("Tree is currently empty.")
    else:
        traversal_running = True
        while traversal_running:
            display_traversal_menu()
            traversal_choice = input("Enter traversal choice: ").strip()

            if traversal_choice == "1":
                print("In-order:  ", tree.inorder())
                traversal_running = False

            elif traversal_choice == "2":
                print("Pre-order: ", tree.preorder())
                traversal_running = False

            elif traversal_choice == "3":
                print("Post-order:", tree.postorder())
                traversal_running = False

            elif traversal_choice == "0":
                traversal_running = False

            else:
                print("Invalid choice, please select a valid option.")


def load_sample_tree(tree):
    sample_keys = [10, 8, 15, 4, 9, 1, 14, 12, 22, 19, 18, 17, 20, 25, 30]
    index = 0
    while index < len(sample_keys):
        key = sample_keys[index]
        try:
            tree.insert(key, "Value-" + str(key))
        except ValueError:
            pass
        index += 1
    print("Sample tree loaded with keys:", sample_keys)


def main():
    tree = DSABinarySearchTree()
    running = True

    while running:
        display_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            input_key = input("Enter key: ").strip()
            input_value = input("Enter value: ").strip()
            try:
                try:
                    key = int(input_key)
                except ValueError:
                    key = input_key

                tree.insert(key, input_value)
                print("Node added successfully.")
            except ValueError as error:
                print("Error:", error)

        elif choice == "2":
            input_key = input("Enter key to delete: ").strip()
            try:
                try:
                    key = int(input_key)
                except ValueError:
                    key = input_key

                tree.delete(key)
                print("Node deleted successfully.")
            except KeyError as error:
                print("Error:", error)

        elif choice == "3":
            input_key = input("Enter key to find: ").strip()
            try:
                try:
                    key = int(input_key)
                except ValueError:
                    key = input_key

                value = tree.find(key)
                print("Found value:", value)
            except KeyError as error:
                print("Error:", error)

        elif choice == "4":
            handle_traversals(tree)

        elif choice == "5":
            print("Tree Height:", tree.height())

        elif choice == "6":
            try:
                print("Min Key:", tree.min())
                print("Max Key:", tree.max())
            except ValueError as error:
                print("Error:", error)

        elif choice == "7":
            print("Balance Score: {:.2f}%".format(tree.balance()))

        elif choice == "8":
            load_sample_tree(tree)

        elif choice == "0":
            print("Exiting...")
            running = False

        else:
            print("Invalid choice, please select a valid option.")


if __name__ == "__main__":
    main()
