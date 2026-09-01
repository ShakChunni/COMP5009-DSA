from DSALinkedList import DSALinkedList
from DSAStack import DSAStack
from DSAQueue import DSAQueue


def display_main_menu():
    print("\n========================================")
    print("      DATA STRUCTURES MAIN MENU")
    print("========================================")
    print("1. Interactive Linked List Menu")
    print("2. Interactive Stack Menu")
    print("3. Interactive Queue Menu")
    print("0. Exit")
    print("========================================")


def display_linked_list_menu():
    print("\n--- Linked List Operations ---")
    print("1. Insert First")
    print("2. Insert Last")
    print("3. Remove First")
    print("4. Remove Last")
    print("5. Peek First")
    print("6. Peek Last")
    print("7. Display List")
    print("0. Return to Main Menu")


def display_stack_menu():
    print("\n--- Stack Operations ---")
    print("1. Push")
    print("2. Pop")
    print("3. Top")
    print("4. Display Stack")
    print("0. Return to Main Menu")


def display_queue_menu():
    print("\n--- Queue Operations ---")
    print("1. Enqueue")
    print("2. Dequeue")
    print("3. Peek")
    print("4. Display Queue")
    print("0. Return to Main Menu")


def handle_linked_list_menu():
    ll = DSALinkedList()
    ll_running = True

    while ll_running:
        display_linked_list_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            val = input("Enter value to insert at first: ")
            ll.insertFirst(val)
            print("Inserted at first:", val)

        elif choice == "2":
            val = input("Enter value to insert at last: ")
            ll.insertLast(val)
            print("Inserted at last:", val)

        elif choice == "3":
            try:
                val = ll.removeFirst()
                print("Removed first value:", val)
            except IndexError as e:
                print("Error:", e)

        elif choice == "4":
            try:
                val = ll.removeLast()
                print("Removed last value:", val)
            except IndexError as e:
                print("Error:", e)

        elif choice == "5":
            try:
                print("Peek first:", ll.peekFirst())
            except IndexError as e:
                print("Error:", e)

        elif choice == "6":
            try:
                print("Peek last:", ll.peekLast())
            except IndexError as e:
                print("Error:", e)

        elif choice == "7":
            print("Current List:", ll)

        elif choice == "0":
            ll_running = False

        else:
            print("Invalid choice, please select an option from the menu.")


def handle_stack_menu():
    stack = DSAStack()
    stack_running = True

    while stack_running:
        display_stack_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            val = input("Enter value to push: ")
            stack.push(val)
            print("Pushed to stack:", val)

        elif choice == "2":
            try:
                val = stack.pop()
                print("Popped value:", val)
            except IndexError as e:
                print("Error:", e)

        elif choice == "3":
            try:
                print("Top value:", stack.top())
            except IndexError as e:
                print("Error:", e)

        elif choice == "4":
            print("Current Stack (top -> bottom):", stack)

        elif choice == "0":
            stack_running = False

        else:
            print("Invalid choice, please select an option from the menu.")


def handle_queue_menu():
    queue = DSAQueue()
    queue_running = True

    while queue_running:
        display_queue_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            val = input("Enter value to enqueue: ")
            queue.enqueue(val)
            print("Enqueued to queue:", val)

        elif choice == "2":
            try:
                val = queue.dequeue()
                print("Dequeued value:", val)
            except IndexError as e:
                print("Error:", e)

        elif choice == "3":
            try:
                print("Peek value:", queue.peek())
            except IndexError as e:
                print("Error:", e)

        elif choice == "4":
            print("Current Queue (front -> rear):", queue)

        elif choice == "0":
            queue_running = False

        else:
            print("Invalid choice, please select an option from the menu.")


def main():
    running = True

    while running:
        display_main_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            handle_linked_list_menu()

        elif choice == "2":
            handle_stack_menu()

        elif choice == "3":
            handle_queue_menu()

        elif choice == "0":
            print("Exiting application...")
            running = False

        else:
            print("Invalid choice, please select an option from the menu.")


if __name__ == "__main__":
    main()
