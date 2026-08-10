# Reference: https://en.wikipedia.org/wiki/Euclidean_algorithm


def _validate_integer(value, name):
    if type(value) is not int:
        raise TypeError(name + " must be an integer")


def gcd_recursive(first_number, second_number):
    _validate_integer(first_number, "first_number")
    _validate_integer(second_number, "second_number")

    if first_number < 0:
        first_number = -first_number

    if second_number < 0:
        second_number = -second_number

    if first_number == 0 and second_number == 0:
        raise ValueError("both numbers cannot be zero")

    if second_number == 0:
        return first_number

    return gcd_recursive(second_number, first_number % second_number)
