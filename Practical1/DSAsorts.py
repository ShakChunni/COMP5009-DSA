#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#

def bubbleSort(A):
    passNum = 0
    sortedArray = False

    while passNum < A.size - 1 and not sortedArray:
        sortedArray = True
        currentIdx = 0

        while currentIdx < A.size - passNum - 1:
            if A[currentIdx] > A[currentIdx + 1]:
                temp = A[currentIdx]
                A[currentIdx] = A[currentIdx + 1]
                A[currentIdx + 1] = temp
                sortedArray = False

            currentIdx += 1

        passNum += 1

def insertionSort(A):
    ...

def selectionSort(A):
    ...

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

