from DSAStack import DSAStack
from DSAQueue import DSAShufflingQueue, DSACircularQueue
from EquationSolver import _parseInfixToPostfix, solve


def demonstrate_stack():
    print("Activity 1: Stack")
    stack = DSAStack(3)
    stack.push(10)
    stack.push(20)
    stack.push(30)
    print("Top:", stack.top())
    print("Pop:", stack.pop())
    print("Count:", stack.getCount())


def demonstrate_shuffling_queue():
    print("\nActivity 1: Shuffling Queue")
    queue = DSAShufflingQueue(3)
    queue.enqueue("A")
    queue.enqueue("B")
    queue.enqueue("C")
    print("Queue:", queue)
    print("Dequeue:", queue.dequeue())
    print("Queue:", queue)


def demonstrate_circular_queue():
    print("\nActivity 2: Circular Queue")
    queue = DSACircularQueue(3)
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    print("Queue:", queue)
    print("Dequeue:", queue.dequeue())
    queue.enqueue(4)
    print("After wrap-around:", queue)


def demonstrate_equation_solver():
    print("\nActivity 3: Equation Solver")
    equation = "( 4 + 2 ) * 3"
    postfix_queue = _parseInfixToPostfix(equation)
    print("Infix:", equation)
    print("Postfix:", postfix_queue)
    print("Answer:", solve(equation))


def main():
    demonstrate_stack()
    #demonstrate_shuffling_queue()
    #demonstrate_circular_queue()
    #demonstrate_equation_solver()


if __name__ == "__main__":
    main()
