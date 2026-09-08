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
    linked_list = DSALinkedList()
    linked_list_menu_running = True

    while linked_list_menu_running:
        display_linked_list_menu()
        list_menu_choice = input("Enter choice: ").strip()

        if list_menu_choice == "1":
            value_to_insert = input("Enter value to insert at first: ")
            linked_list.insertFirst(value_to_insert)
            print("Inserted at first:", value_to_insert)

        elif list_menu_choice == "2":
            value_to_insert = input("Enter value to insert at last: ")
            linked_list.insertLast(value_to_insert)
            print("Inserted at last:", value_to_insert)

        elif list_menu_choice == "3":
            try:
                removed_value = linked_list.removeFirst()
                print("Removed first value:", removed_value)
            except IndexError as error:
                print("Error:", error)

        elif list_menu_choice == "4":
            try:
                removed_value = linked_list.removeLast()
                print("Removed last value:", removed_value)
            except IndexError as error:
                print("Error:", error)

        elif list_menu_choice == "5":
            try:
                print("Peek first:", linked_list.peekFirst())
            except IndexError as error:
                print("Error:", error)

        elif list_menu_choice == "6":
            try:
                print("Peek last:", linked_list.peekLast())
            except IndexError as error:
                print("Error:", error)

        elif list_menu_choice == "7":
            print("Current List:", linked_list)

        elif list_menu_choice == "0":
            linked_list_menu_running = False

        else:
            print("Invalid choice, please select an option from the menu.")


def handle_stack_menu():
    stack = DSAStack()
    stack_menu_running = True

    while stack_menu_running:
        display_stack_menu()
        stack_menu_choice = input("Enter choice: ").strip()

        if stack_menu_choice == "1":
            value_to_push = input("Enter value to push: ")
            stack.push(value_to_push)
            print("Pushed to stack:", value_to_push)

        elif stack_menu_choice == "2":
            try:
                popped_value = stack.pop()
                print("Popped value:", popped_value)
            except IndexError as error:
                print("Error:", error)

        elif stack_menu_choice == "3":
            try:
                print("Top value:", stack.top())
            except IndexError as error:
                print("Error:", error)

        elif stack_menu_choice == "4":
            print("Current Stack (top -> bottom):", stack)

        elif stack_menu_choice == "0":
            stack_menu_running = False

        else:
            print("Invalid choice, please select an option from the menu.")


def handle_queue_menu():
    queue = DSAQueue()
    queue_menu_running = True

    while queue_menu_running:
        display_queue_menu()
        queue_menu_choice = input("Enter choice: ").strip()

        if queue_menu_choice == "1":
            value_to_enqueue = input("Enter value to enqueue: ")
            queue.enqueue(value_to_enqueue)
            print("Enqueued to queue:", value_to_enqueue)

        elif queue_menu_choice == "2":
            try:
                dequeued_value = queue.dequeue()
                print("Dequeued value:", dequeued_value)
            except IndexError as error:
                print("Error:", error)

        elif queue_menu_choice == "3":
            try:
                print("Peek value:", queue.peek())
            except IndexError as error:
                print("Error:", error)

        elif queue_menu_choice == "4":
            print("Current Queue (front -> rear):", queue)

        elif queue_menu_choice == "0":
            queue_menu_running = False

        else:
            print("Invalid choice, please select an option from the menu.")


def main():
    main_menu_running = True

    while main_menu_running:
        display_main_menu()
        main_menu_choice = input("Enter choice: ").strip()

        if main_menu_choice == "1":
            handle_linked_list_menu()

        elif main_menu_choice == "2":
            handle_stack_menu()

        elif main_menu_choice == "3":
            handle_queue_menu()

        elif main_menu_choice == "0":
            print("Exiting application...")
            main_menu_running = False

        else:
            print("Invalid choice, please select an option from the menu.")


if __name__ == "__main__":
    main()
