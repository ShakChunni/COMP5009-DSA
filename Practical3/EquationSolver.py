import numpy as np

from DSAStack import DSAStack
from DSAQueue import DSAQueue, DSACircularQueue


def _precedenceOf(theOp):
    if theOp == '+' or theOp == '-':
        return 1
    if theOp == '*' or theOp == '/':
        return 2
    return 0


def _executeOperation(op, op1, op2):
    if op == '+':
        return op1 + op2
    if op == '-':
        return op1 - op2
    if op == '*':
        return op1 * op2
    if op == '/':
        if op2 == 0:
            raise ZeroDivisionError("Division by zero in equation")
        return op1 / op2
    raise ValueError("Unsupported operator: " + str(op))


def _tokenize(equation):
    if type(equation) is not str:
        raise TypeError("Equation must be a string")

    tokens = np.empty(len(equation) + 1, dtype=object)
    token_count = 0
    current_token = ""
    index = 0

    while index < len(equation):
        character = equation[index]

        if character == ' ':
            if current_token != "":
                tokens[token_count] = current_token
                token_count += 1
                current_token = ""
        elif (character == '(' or character == ')' or character == '+' or
              character == '-' or character == '*' or character == '/'):
            if current_token != "":
                tokens[token_count] = current_token
                token_count += 1
                current_token = ""
            tokens[token_count] = character
            token_count += 1
        else:
            current_token += character

        index += 1

    if current_token != "":
        tokens[token_count] = current_token
        token_count += 1

    return tokens, token_count


def _parseInfixToPostfix(equation, queue_class=DSACircularQueue):
    tokens, token_count = _tokenize(equation)
    if token_count == 0:
        raise ValueError("Equation cannot be empty")

    operator_stack = DSAStack(token_count)
    postfix_queue = queue_class(token_count)
    token_index = 0

    while token_index < token_count:
        token = tokens[token_index]

        if token == '(':
            operator_stack.push(token)
        elif token == ')':
            found_open = False
            while not operator_stack.isEmpty():
                operator = operator_stack.pop()
                if operator == '(':
                    found_open = True
                    break
                postfix_queue.enqueue(operator)
            if not found_open:
                raise ValueError("Mismatched brackets")
        elif (token == '+' or token == '-' or token == '*' or token == '/'):
            while (not operator_stack.isEmpty() and
                   operator_stack.top() != '(' and
                   _precedenceOf(operator_stack.top()) >= _precedenceOf(token)):
                postfix_queue.enqueue(operator_stack.pop())
            operator_stack.push(token)
        else:
            postfix_queue.enqueue(float(token))

        token_index += 1

    while not operator_stack.isEmpty():
        operator = operator_stack.pop()
        if operator == '(':
            raise ValueError("Mismatched brackets")
        postfix_queue.enqueue(operator)

    return postfix_queue


def _evaluatePostfix(postfixQueue):
    if not isinstance(postfixQueue, DSAQueue):
        raise TypeError("postfixQueue must be an instance of DSAQueue")
    if postfixQueue.isEmpty():
        raise ValueError("Postfix equation cannot be empty")

    operand_stack = DSAStack(postfixQueue.getCount())

    while not postfixQueue.isEmpty():
        term = postfixQueue.dequeue()

        if isinstance(term, (int, float)):
            operand_stack.push(float(term))
        elif (isinstance(term, str) and
              (term == '+' or term == '-' or term == '*' or term == '/')):
            if operand_stack.getCount() < 2:
                raise ValueError("Insufficient operands")
            op2 = operand_stack.pop()
            op1 = operand_stack.pop()
            operand_stack.push(_executeOperation(term, op1, op2))
        else:
            raise ValueError("Invalid postfix term")

    if operand_stack.getCount() != 1:
        raise ValueError("Invalid equation")
    return operand_stack.pop()


def solve(equation, queue_class=DSACircularQueue):
    postfix_queue = _parseInfixToPostfix(equation, queue_class)
    return _evaluatePostfix(postfix_queue)
