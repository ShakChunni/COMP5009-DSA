def _validate_non_negative_integer(value, name):
    if type(value) is not int:
        raise TypeError(name + " must be an integer")

    if value < 0:
        raise ValueError(name + " must not be negative")


def factorial_iterative(n):
    _validate_non_negative_integer(n, "n")

    factorial = 1
    current_value = n

    while current_value >= 2:
        factorial = factorial * current_value
        current_value -= 1

    return factorial


def factorial_recursive(n):
    _validate_non_negative_integer(n, "n")

    factorial = 1

    if n == 0:
        factorial = 1
    else:
        factorial = n * factorial_recursive(n - 1)

    return factorial


def fibonacci_iterative(n):
    _validate_non_negative_integer(n, "n")

    fibonacci_value = 0
    current_value = 1
    previous_value = 0

    if n == 0:
        fibonacci_value = 0
    elif n == 1:
        fibonacci_value = 1
    else:
        current_index = 2

        while current_index <= n:
            fibonacci_value = current_value + previous_value
            previous_value = current_value
            current_value = fibonacci_value
            current_index += 1

    return fibonacci_value


def fibonacci_recursive(n):
    _validate_non_negative_integer(n, "n")

    fibonacci_value = 0

    if n == 0:
        fibonacci_value = 0
    elif n == 1:
        fibonacci_value = 1
    else:
        fibonacci_value = (fibonacci_recursive(n - 1)
                           + fibonacci_recursive(n - 2))

    return fibonacci_value
