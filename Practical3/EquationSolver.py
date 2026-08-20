#
# Data Structures and Algorithms
# Practical 3: Stacks and Queues
# EquationSolver Implementation (Infix to Postfix Conversion & Evaluation)
#

from DSAStack import DSAStack
from DSAQueue import DSAQueue, DSACircularQueue, DSAShufflingQueue


def _precedenceOf(theOp):
    """
    Helper function for _parseInfixToPostfix().
    Returns the precedence (as an integer) of the operator.
      '+', '-' -> 1
      '*', '/' -> 2
    """
    if theOp == '+' or theOp == '-':
        return 1
    elif theOp == '*' or theOp == '/':
        return 2
    else:
        return 0


def _executeOperation(op, op1, op2):
    """
    Helper function for _evaluatePostfix().
    Executes the binary operation:
      op1 + op2
      op1 - op2
      op1 * op2
      op1 / op2
    """
    if op == '+':
        return op1 + op2
    elif op == '-':
        return op1 - op2
    elif op == '*':
        return op1 * op2
    elif op == '/':
        if op2 == 0:
            raise ZeroDivisionError("Division by zero in equation")
        return op1 / op2
    else:
        raise ValueError("Unsupported operator: " + str(op))


def _tokenize(equation):
    """
    Manual tokenization of equation string without regex.
    Handles spaces between tokens as well as adjacent brackets/operators.
    """
    if type(equation) is not str:
        raise TypeError("Equation must be a string")

    tokens = []
    current_token = ""
    index = 0

    while index < len(equation):
        ch = equation[index]

        if ch == ' ':
            if len(current_token) > 0:
                tokens.append(current_token)
                current_token = ""
        elif ch == '(' or ch == ')' or ch == '+' or ch == '-' or ch == '*' or ch == '/':
            if len(current_token) > 0:
                tokens.append(current_token)
                current_token = ""
            tokens.append(ch)
        else:
            current_token = current_token + ch

        index += 1

    if len(current_token) > 0:
        tokens.append(current_token)

    return tokens


def _parseInfixToPostfix(equation, queue_class=DSACircularQueue):
    """
    Converts an infix expression string into a postfix DSAQueue of terms.
    Stores operands as floats and operators as characters/strings.
    """
    tokens = _tokenize(equation)
    if len(tokens) == 0:
        raise ValueError("Equation cannot be empty")

    op_stack = DSAStack(len(tokens) + 20)
    postfix_queue = queue_class(len(tokens) + 20)

    token_idx = 0
    while token_idx < len(tokens):
        token = tokens[token_idx]

        if token == '(':
            op_stack.push(token)

        elif token == ')':
            found_matching_open = False
            while not op_stack.isEmpty():
                top_op = op_stack.pop()
                if top_op == '(':
                    found_matching_open = True
                    break
                postfix_queue.enqueue(top_op)

            if not found_matching_open:
                raise ValueError("Mismatched brackets: no associated '(' found for ')'")

        elif token == '+' or token == '-' or token == '*' or token == '/':
            while (not op_stack.isEmpty()) and (op_stack.top() != '(') and (
                    _precedenceOf(op_stack.top()) >= _precedenceOf(token)):
                postfix_queue.enqueue(op_stack.pop())

            op_stack.push(token)

        else:
            try:
                numeric_val = float(token)
            except ValueError:
                raise ValueError("Invalid numeric token: '" + str(token) + "'")
            postfix_queue.enqueue(numeric_val)

        token_idx += 1

    # Transfer remaining operators from stack to queue
    while not op_stack.isEmpty():
        remaining_op = op_stack.pop()
        if remaining_op == '(' or remaining_op == ')':
            raise ValueError("Mismatched brackets: unclosed '(' in equation")
        postfix_queue.enqueue(remaining_op)

    return postfix_queue


def _evaluatePostfix(postfixQueue):
    """
    Evaluates a postfix DSAQueue containing floats and operator characters.
    Returns the final double/float result.
    """
    if not isinstance(postfixQueue, DSAQueue):
        raise TypeError("postfixQueue must be an instance of DSAQueue")

    operand_stack = DSAStack(postfixQueue.getCount() + 20)

    while not postfixQueue.isEmpty():
        term = postfixQueue.dequeue()

        if isinstance(term, (int, float)):
            operand_stack.push(float(term))
        elif isinstance(term, str) and (term == '+' or term == '-' or term == '*' or term == '/'):
            if operand_stack.getCount() < 2:
                raise ValueError("Invalid expression: insufficient operands for operator '" + term + "'")

            op2 = operand_stack.pop()
            op1 = operand_stack.pop()
            result = _executeOperation(term, op1, op2)
            operand_stack.push(result)
        else:
            raise ValueError("Invalid term encountered during postfix evaluation: " + str(term))

    if operand_stack.getCount() != 1:
        raise ValueError("Invalid expression: extra operands remaining on stack")

    return operand_stack.pop()


def solve(equation, queue_class=DSACircularQueue):
    """
    Takes a mathematical infix equation string and solves it:
      1. Converts infix equation to postfix DSAQueue via _parseInfixToPostfix()
      2. Evaluates postfix DSAQueue via _evaluatePostfix()
    Returns the final calculated float result.
    """
    postfix_queue = _parseInfixToPostfix(equation, queue_class=queue_class)
    return _evaluatePostfix(postfix_queue)


if __name__ == "__main__":
    print("=== Testing EquationSolver ===")
    test_eqns = [
        "3 * 4",
        "2 - 4 + 3",
        "4 + 2 * 3",
        "( 4 + 2 ) * 3",
        "( ( 2 - 3 ) / 4 * ( 1 + 9 ) ) * 2",
        "( 10.3 * ( 14 + 3.2 ) ) / ( 5 + 2 - 4 * 3 )"
    ]

    for eq in test_eqns:
        pfix = _parseInfixToPostfix(eq)
        ans = solve(eq)
        print("Infix:   ", eq)
        print("Postfix: ", pfix)
        print("Result:  ", ans)
        print("-" * 40)
