from DSALinkedList import DSALinkedList
from DSAStack import DSAStack
from DSAQueue import DSAQueue


def display_menu():
    print("\n========== Linked List Menu ==========")
    print("1. Insert First")
    print("2. Insert Last")
    print("3. Remove First")
    print("4. Remove Last")
    print("5. Peek First")
    print("6. Peek Last")
    print("7. Display List")
    print("8. Run Stack & Queue Test")
    print("0. Exit")
    print("=======================================")


def run_stack_and_queue_demo():
    print("\n--- Stack Demo (LinkedList-backed) ---")
    stack = DSAStack()
    stack.push(10)
    stack.push(20)
    stack.push(30)
    print("Stack:", stack)
    print("Top:", stack.top())
    print("Pop:", stack.pop())
    print("Stack now:", stack)

    print("\n--- Queue Demo (LinkedList-backed) ---")
    queue = DSAQueue()
    queue.enqueue("First")
    queue.enqueue("Second")
    queue.enqueue("Third")
    print("Queue:", queue)
    print("Peek:", queue.peek())
    print("Dequeue:", queue.dequeue())
    print("Queue now:", queue)


def main():
    ll = DSALinkedList()
    running = True

    while running:
        display_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            val = input("Enter value to insert at first: ")
            ll.insertFirst(val)
            print("Inserted successfully.")

        elif choice == "2":
            val = input("Enter value to insert at last: ")
            ll.insertLast(val)
            print("Inserted successfully.")

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

        elif choice == "8":
            run_stack_and_queue_demo()

        elif choice == "0":
            print("Exiting...")
            running = False

        else:
            print("Invalid choice, please enter a valid option.")


if __name__ == "__main__":
    main()
