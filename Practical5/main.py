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
            sub_choice = input("Enter traversal choice: ").strip()

            if sub_choice == "1":
                print("In-order:  ", tree.inorder())
                traversal_running = False

            elif sub_choice == "2":
                print("Pre-order: ", tree.preorder())
                traversal_running = False

            elif sub_choice == "3":
                print("Post-order:", tree.postorder())
                traversal_running = False

            elif sub_choice == "0":
                traversal_running = False

            else:
                print("Invalid choice, please select a valid option.")


def load_sample_tree(tree):
    # Sample keys from lecture slide 26: 50, 16, 7, 89, 70, 45, 10, 66, 95
    sample_keys = [50, 16, 7, 89, 70, 45, 10, 66, 95]
    index = 0
    while index < len(sample_keys):
        key = sample_keys[index]
        try:
            tree.insert(key, "Val-" + str(key))
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
            key_input = input("Enter key: ").strip()
            val_input = input("Enter value: ").strip()
            try:
                # If key looks like an integer, store as int for proper numeric sorting
                try:
                    parsed_key = int(key_input)
                except ValueError:
                    parsed_key = key_input

                tree.insert(parsed_key, val_input)
                print("Node added successfully.")
            except ValueError as e:
                print("Error:", e)

        elif choice == "2":
            key_input = input("Enter key to delete: ").strip()
            try:
                try:
                    parsed_key = int(key_input)
                except ValueError:
                    parsed_key = key_input

                tree.delete(parsed_key)
                print("Node deleted successfully.")
            except KeyError as e:
                print("Error:", e)

        elif choice == "3":
            key_input = input("Enter key to find: ").strip()
            try:
                try:
                    parsed_key = int(key_input)
                except ValueError:
                    parsed_key = key_input

                val = tree.find(parsed_key)
                print("Found value:", val)
            except KeyError as e:
                print("Error:", e)

        elif choice == "4":
            handle_traversals(tree)

        elif choice == "5":
            print("Tree Height:", tree.height())

        elif choice == "6":
            try:
                print("Min Key:", tree.min())
                print("Max Key:", tree.max())
            except ValueError as e:
                print("Error:", e)

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
