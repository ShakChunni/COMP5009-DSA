#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#

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
    ...

def mergeSortRecurse(A, leftIdx, rightIdx):
    ...

def merge(A, leftIdx, midIdx, rightIdx):
    ...

def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    ...

def quickSortRecurse(A, leftIdx, rightIdx):
    ...

def doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    ...
