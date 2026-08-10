import time

from factorial_fibonacci import (factorial_iterative,
                                 factorial_recursive,
                                 fibonacci_iterative,
                                 fibonacci_recursive)
from gcd import gcd_recursive
from number_conversion import decimal_to_base
from towers_of_hanoi import towers


def _time_call(function, value):
    start_time = time.perf_counter()
    result = function(value)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return result, elapsed_time


def run_factorial_fibonacci_examples():
    print("Activity 1: Factorial and Fibonacci")
    print("5 factorial, iterative:", factorial_iterative(5))
    print("5 factorial, recursive:", factorial_recursive(5))
    print("10th Fibonacci, iterative:", fibonacci_iterative(10))
    print("10th Fibonacci, recursive:", fibonacci_recursive(10))

    print("Performance samples:")
    test_value = 5

    while test_value <= 30:
        _, factorial_recursive_time = _time_call(
            factorial_recursive, test_value)
        _, fibonacci_iterative_time = _time_call(
            fibonacci_iterative, test_value)
        _, fibonacci_recursive_time = _time_call(
            fibonacci_recursive, test_value)

        print("n=", test_value,
              "factorial recursive seconds=", factorial_recursive_time,
              "Fibonacci iterative seconds=", fibonacci_iterative_time,
              "Fibonacci recursive seconds=", fibonacci_recursive_time)
        test_value += 5


def run_gcd_examples():
    print("Activity 2: Greatest Common Divisor")
    print("gcd(48, 18)=", gcd_recursive(48, 18))


def run_conversion_examples():
    print("Activity 3: Number Conversions")
    print("255 in base 2=", decimal_to_base(255, 2))
    print("255 in base 16=", decimal_to_base(255, 16))


def run_exception_examples():
    print("Activity 4: Exception Handling")

    try:
        factorial_recursive(-1)
    except (TypeError, ValueError) as error:
        print("Factorial exception handled:", error)

    try:
        gcd_recursive(0, 0)
    except (TypeError, ValueError) as error:
        print("GCD exception handled:", error)

    try:
        decimal_to_base(10, 1)
    except (TypeError, ValueError) as error:
        print("Conversion exception handled:", error)


def run_hanoi_example():
    print("Activity 5: Towers of Hanoi")
    disk_text = input("Enter the number of disks: ")
    number_of_disks = int(disk_text)
    towers(number_of_disks, 1, 3)


def main():
    try:
        run_factorial_fibonacci_examples()
        run_gcd_examples()
        run_conversion_examples()
        run_exception_examples()
        run_hanoi_example()
    except (TypeError, ValueError, RecursionError) as error:
        print("Input or recursion exception handled:", error)


if __name__ == "__main__":
    main()
