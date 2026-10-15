# Practical 9: Sorting performance

Times are in milliseconds. These are measured results from `python3 benchmark.py`, not estimated values. Each case runs three times; the first run is discarded and the remaining two are averaged. Only sorting is timed, excluding array creation, printing and the order check. Seeds 42, 43 and 44 give the same input arrays to each algorithm. Times can change between runs and computers.

`a` = ascending, `d` = descending, `r` = random.

| Size | Input | Bubble | Insertion | Selection | Merge | Quick left | Quick median3 | Quick random |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 250 | a | 0.019 | 0.019 | 2.195 | 0.371 | 1.242 | 0.164 | 0.226 |
| 250 | d | 5.451 | 5.013 | 2.284 | 0.350 | 2.493 | 0.272 | 0.236 |
| 250 | r | 3.658 | 2.540 | 2.933 | 0.402 | 0.226 | 0.215 | 0.222 |
| 500 | a | 0.048 | 0.045 | 9.334 | 0.787 | 4.881 | 0.405 | 0.538 |
| 500 | d | 22.200 | 20.401 | 8.792 | 0.802 | 10.887 | 0.700 | 0.593 |
| 500 | r | 16.373 | 10.110 | 8.669 | 0.925 | 0.505 | 0.501 | 0.658 |
| 1000 | a | 0.101 | 0.078 | 40.741 | 1.777 | 20.183 | 1.376 | 1.245 |
| 1000 | d | 110.538 | 89.967 | 36.998 | 1.918 | 44.832 | 1.693 | 1.259 |
| 1000 | r | 67.844 | 43.046 | 37.931 | 2.178 | 1.308 | 1.257 | 1.324 |
| 2000 | a | 0.165 | 0.153 | 155.343 | 4.027 | 77.748 | 2.081 | 2.801 |
| 2000 | d | 392.353 | 343.776 | 143.513 | 3.976 | 185.991 | 3.945 | 2.989 |
| 2000 | r | 276.884 | 183.436 | 139.538 | 4.596 | 2.621 | 2.521 | 2.786 |

Bubble and insertion sort were fastest on ascending input because their best case is O(n). Their random and descending results grew much faster, consistent with O(n squared), while selection sort showed O(n squared) behaviour for every condition. Merge Sort stayed relatively consistent across input conditions, matching O(n log n) time, but needs O(n) extra array space and is stable because equal values are taken from the left half first. Leftmost-pivot QuickSort was much slower on ascending and descending input because its partitions become unbalanced, giving O(n squared) time. Median-of-three and random pivots performed much better on these inputs and were generally fastest on random data; QuickSort has average O(n log n) time, but every pivot strategy can still have an O(n squared) worst case. QuickSort swaps within the original array and is not stable. This implementation recurses on the smaller partition and loops over the larger one, keeping recursion space O(log n) even when partitions are unbalanced. Measured timings support these trends, but are not exact proofs of complexity.

Run the harness, for example:

```bash
python3 SortsTestHarness.py 20 ma qd tr un
```

Sort codes: `b` bubble, `i` insertion, `s` selection, `m` merge, `q` leftmost QuickSort, `t` median-of-three QuickSort, `u` random QuickSort. Input codes: `a` ascending, `d` descending, `r` random, `n` nearly sorted.

The Practical9 harness adds the two QuickSort options, checks every adjacent pair, and fixes the warm-up averaging. It also times only the sorting call and seeds the random generator. The Practical1 files are unchanged.
