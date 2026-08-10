# Reference: https://en.wikipedia.org/wiki/Positional_notation#Base_conversion

DIGITS = "0123456789ABCDEF"


def _validate_conversion_input(decimal_number, base):
    if type(decimal_number) is not int:
        raise TypeError("decimal_number must be an integer")

    if type(base) is not int:
        raise TypeError("base must be an integer")

    if decimal_number < 0:
        raise ValueError("decimal_number must not be negative")

    if base < 2 or base > 16:
        raise ValueError("base must be between 2 and 16")


def decimal_to_base(decimal_number, base):
    _validate_conversion_input(decimal_number, base)

    if decimal_number == 0:
        return "0"

    if decimal_number < base:
        return DIGITS[decimal_number]

    leading_digits = decimal_to_base(decimal_number // base, base)
    final_digit = DIGITS[decimal_number % base]
    return leading_digits + final_digit
