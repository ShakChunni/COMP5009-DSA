#
# Data Structures and Algorithms
# Practical 3: Stacks and Queues
# Main Demonstration Program
#

from DSAStack import DSAStack
from DSAQueue import DSAShufflingQueue, DSACircularQueue
from EquationSolver import solve, _parseInfixToPostfix


def run_stack_demonstration():
    print("==================================================")
    print("Activity 1: DSAStack Demonstration")
    print("==================================================")
    stack = DSAStack(5)
    print("Created DSAStack with capacity 5. isEmpty():", stack.isEmpty())

    print("Pushing elements: 10.5, 20.2, 30.7, 40.0")
    stack.push(10.5)
    stack.push(20.2)
    stack.push(30.7)
    stack.push(40.0)

    stack.display()
    print("Current count:", stack.getCount())
    print("Top element (top/peek):", stack.top())

    print("\nPopping 2 elements:")
    print("Popped:", stack.pop())
    print("Popped:", stack.pop())
    stack.display()
    print("Current count:", stack.getCount())


def run_queue_demonstration():
    print("\n==================================================")
    print("Activities 1 & 2: DSAQueue Polymorphism Demonstration")
    print("==================================================")

    for queue_name, queue in [("Shuffling Queue (DSAShufflingQueue)", DSAShufflingQueue(4)),
                              ("Circular Queue (DSACircularQueue)", DSACircularQueue(4))]:
        print(f"\n--- Testing {queue_name} ---")
        print("Initial isEmpty():", queue.isEmpty())

        print("Enqueuing: 'Job 1', 'Job 2', 'Job 3'")
        queue.enqueue("Job 1")
        queue.enqueue("Job 2")
        queue.enqueue("Job 3")
        queue.display()
        print("Peek front element:", queue.peek())

        print("Dequeued:", queue.dequeue())
        queue.display()

        print("Enqueuing: 'Job 4', 'Job 5'")
        queue.enqueue("Job 4")
        queue.enqueue("Job 5")
        queue.display()
        print("isFull():", queue.isFull())

        print("Emptying queue:")
        while not queue.isEmpty():
            print("  Dequeued:", queue.dequeue())
        print("Final isEmpty():", queue.isEmpty())


def run_equation_solver_demonstration():
    print("\n==================================================")
    print("Activity 3: Equation Solver Demonstration")
    print("==================================================")

    test_equations = [
        "3 * 4",
        "2 - 4 + 3",
        "4 + 2 * 3",
        "( 4 + 2 ) * 3",
        "( ( 2 - 3 ) / 4 * ( 1 + 9 ) ) * 2",
        "( 10.3 * ( 14 + 3.2 ) ) / ( 5 + 2 - 4 * 3 )"
    ]

    print("Demonstrating worksheet examples (using both Circular & Shuffling queues):\n")
    for eq in test_equations:
        postfix_cq = _parseInfixToPostfix(eq, queue_class=DSACircularQueue)
        result_cq = solve(eq, queue_class=DSACircularQueue)
        result_sq = solve(eq, queue_class=DSAShufflingQueue)

        print(f"Infix Equation:     {eq}")
        print(f"Postfix Conversion: {postfix_cq}")
        print(f"CircularQueue Sol:  {result_cq}")
        print(f"ShufflingQueue Sol: {result_sq}")
        print("-" * 50)


def run_interactive_solver():
    print("\n==================================================")
    print("Interactive Equation Solver")
    print("==================================================")
    user_input = input("Enter an infix equation to solve (or press Enter to skip): ").strip()
    if user_input:
        try:
            postfix = _parseInfixToPostfix(user_input)
            result = solve(user_input)
            print(f"Postfix: {postfix}")
            print(f"Answer:  {result}")
        except Exception as error:
            print(f"Error evaluating equation: {error}")


def main():
    try:
        run_stack_demonstration()
       # run_queue_demonstration()
       # run_equation_solver_demonstration()
       # run_interactive_solver()
    except Exception as error:
        print(f"Demonstration encountered error: {error}")


if __name__ == "__main__":
    main()
