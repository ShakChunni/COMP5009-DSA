# Based on the sorting interfaces in my Practical 1; algorithms implemented here.
# Reference: Cormen et al., Introduction to Algorithms, 4th ed., 2022.


def mergeSort(records):
    """Stable, top-down Merge Sort by transport time; modify the array in place."""
    temporary = [None] * len(records)

    def recurse(left, right):
        if left >= right:
            return
        middle = (left + right) // 2
        recurse(left, middle)
        recurse(middle + 1, right)
        first, second = left, middle + 1
        for target in range(left, right + 1):
            if (first <= middle and
                    (second > right or records[first].transport_time <= records[second].transport_time)):
                temporary[target] = records[first]
                first += 1
            else:
                temporary[target] = records[second]
                second += 1
        for index in range(left, right + 1):
            records[index] = temporary[index]

    recurse(0, len(records) - 1)
    return records


def quickSort(records):
    """Median-of-three pivot, Hoare partition; equal keys progress on both sides.

    Recurse on the smaller partition and loop over the larger one to bound the
    recursion stack by O(log n), even when partitions are unbalanced.
    """
    def median(first, middle, last):
        if first < middle:
            if middle < last:
                return middle
            return last if first < last else first
        if first < last:
            return first
        return last if middle < last else middle

    def partition(left, right):
        pivot = median(records[left].transport_time,
                       records[(left + right) // 2].transport_time,
                       records[right].transport_time)
        first, second = left - 1, right + 1
        while True:
            first += 1
            while records[first].transport_time < pivot:
                first += 1
            second -= 1
            while records[second].transport_time > pivot:
                second -= 1
            if first >= second:
                return second
            records[first], records[second] = records[second], records[first]

    def recurse(left, right):
        while left < right:
            boundary = partition(left, right)
            if boundary - left < right - boundary:
                recurse(left, boundary)
                left = boundary + 1
            else:
                recurse(boundary + 1, right)
                right = boundary

    recurse(0, len(records) - 1)
    return records


def isSorted(records):
    for index in range(1, len(records)):
        if records[index - 1].transport_time > records[index].transport_time:
            return False
    return True
