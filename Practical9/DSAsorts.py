#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#

import numpy as np
import random

def bubbleSort(A):
    pass_number = 0
    is_sorted = False

    while pass_number < A.size - 1 and not is_sorted:
        is_sorted = True
        current_index = 0

        while current_index < A.size - pass_number - 1:
            if A[current_index] > A[current_index + 1]:
                temp = A[current_index]
                A[current_index] = A[current_index + 1]
                A[current_index + 1] = temp
                is_sorted = False

            current_index += 1

        pass_number += 1

def insertionSort(A):
    current_position = 1

    while current_position < A.size:
        scan_index = current_position

        while (scan_index > 0 and A[scan_index - 1] > A[scan_index]):
            temp = A[scan_index]
            A[scan_index] = A[scan_index - 1]
            A[scan_index - 1] = temp
            scan_index -= 1

        current_position += 1

def selectionSort(A):
    current_position = 0

    while current_position < A.size - 1:
        minimum_index = current_position
        scan_index = current_position + 1

        while scan_index < A.size:
            if A[scan_index] < A[minimum_index]:
                minimum_index = scan_index

            scan_index += 1

        temp = A[current_position]
        A[current_position] = A[minimum_index]
        A[minimum_index] = temp
        current_position += 1

def mergeSort(A):
    """ mergeSort - front-end for kick-starting the recursive algorithm
    """
    mergeSortRecurse(A, 0, A.size - 1)

def mergeSortRecurse(A, left_index, right_index):
    if left_index < right_index:
        middle_index = (left_index + right_index) // 2
        mergeSortRecurse(A, left_index, middle_index)
        mergeSortRecurse(A, middle_index + 1, right_index)
        merge(A, left_index, middle_index, right_index)

def merge(A, left_index, middle_index, right_index):
    temporary = np.empty(right_index - left_index + 1, dtype=A.dtype)
    left_position = left_index
    right_position = middle_index + 1
    temporary_position = 0

    while left_position <= middle_index and right_position <= right_index:
        if A[left_position] <= A[right_position]:
            temporary[temporary_position] = A[left_position]
            left_position += 1
        else:
            temporary[temporary_position] = A[right_position]
            right_position += 1
        temporary_position += 1

    while left_position <= middle_index:
        temporary[temporary_position] = A[left_position]
        left_position += 1
        temporary_position += 1

    while right_position <= right_index:
        temporary[temporary_position] = A[right_position]
        right_position += 1
        temporary_position += 1

    temporary_position = 0
    while temporary_position < temporary.size:
        A[left_index + temporary_position] = temporary[temporary_position]
        temporary_position += 1

def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    quickSortRecurse(A, 0, A.size - 1, "left")

def quickSortMedian3(A):
    quickSortRecurse(A, 0, A.size - 1, "median")

def quickSortRandom(A):
    quickSortRecurse(A, 0, A.size - 1, "random")

def _choosePivot(A, left_index, right_index, strategy):
    if strategy == "random":
        return random.randint(left_index, right_index)
    if strategy == "median":
        middle_index = (left_index + right_index) // 2
        if A[left_index] <= A[middle_index]:
            if A[middle_index] <= A[right_index]:
                return middle_index
            if A[left_index] <= A[right_index]:
                return right_index
            return left_index
        if A[left_index] <= A[right_index]:
            return left_index
        if A[middle_index] <= A[right_index]:
            return right_index
        return middle_index
    return left_index

def quickSortRecurse(A, left_index, right_index, strategy="left"):
    while left_index < right_index:
        pivot_index = _choosePivot(A, left_index, right_index, strategy)
        pivot_position = doPartitioning(A, left_index, right_index, pivot_index)

        if pivot_position - left_index < right_index - pivot_position:
            quickSortRecurse(A, left_index, pivot_position - 1, strategy)
            left_index = pivot_position + 1
        else:
            quickSortRecurse(A, pivot_position + 1, right_index, strategy)
            right_index = pivot_position - 1

def doPartitioning(A, left_index, right_index, pivot_index):
    pivot_value = A[pivot_index]
    temporary = A[pivot_index]
    A[pivot_index] = A[right_index]
    A[right_index] = temporary
    store_index = left_index
    scan_index = left_index

    while scan_index < right_index:
        if A[scan_index] < pivot_value:
            temporary = A[scan_index]
            A[scan_index] = A[store_index]
            A[store_index] = temporary
            store_index += 1
        scan_index += 1

    temporary = A[store_index]
    A[store_index] = A[right_index]
    A[right_index] = temporary
    return store_index
