# Empirical Analysis of Insertion Sort

CS314 Analysis of Algorithms, Lecture 1 mini project.

The project implements insertion sort in C++, counts its comparisons and shifts, measures its running time on sorted, reverse-sorted and random inputs for n = 100 to 5,000, and compares the results with merge sort and with the O(n) and O(n^2) growth curves.

## Structure

```
include/sorts.hpp      insertion sort and merge sort, both returning operation counts
src/benchmark.cpp      experiment driver, writes a CSV to standard output
tests/test_sorts.cpp   unit tests (no external framework)
scripts/plot.py        draws the figures and prints log-log slopes (matplotlib)
results/results.csv    measurements produced by the benchmark
figures/               plots produced by plot.py
Makefile               build, test, run and plot targets
```

## Requirements

- g++ with C++17 support
- make (optional, the plain commands are given below)
- Python 3 with matplotlib (only for the plots)

## Build, test and run

With make:

```
make test
make run
make plot
```

Without make:

```
g++ -std=c++17 -O2 -Wall -Wextra -Iinclude tests/test_sorts.cpp -o test_sorts
./test_sorts
g++ -std=c++17 -O2 -Wall -Wextra -Iinclude src/benchmark.cpp -o benchmark
./benchmark > results/results.csv
python3 scripts/plot.py results/results.csv figures
```

## What is counted

- comparisons: comparisons between two array elements.
- moves: for insertion sort, the number of shifts of one element to the right; for merge sort, the number of elements written while merging.

For insertion sort on an array of n elements:

| Input | Comparisons | Shifts | Complexity |
|---|---|---|---|
| sorted | n - 1 | 0 | Ω(n) |
| reverse sorted | n(n - 1)/2 | n(n - 1)/2 | O(n^2) |
| random | about n^2/4 | about n^2/4 | Θ(n^2) |

## Experiment design

- Sizes: n = 100, 500, 1000, 1500, ..., 5000.
- Inputs: sorted, reverse sorted, random permutation of 1..n (fixed seed 42).
- Each measurement is the median of 21 runs, each on a fresh copy of the input. Only the sort itself is timed.
- Comparison and move counts are averages over the same runs.
- Every run checks that the output is sorted.

## Output format

`results/results.csv` has the columns `algorithm,input,n,comparisons,moves,time_us`.

## Tests

`tests/test_sorts.cpp` checks:

- both sorts against `std::sort` on edge cases (empty, single element, duplicates, negative values) and 200 random arrays;
- the operation counts for the lecture examples: [7, 3, 9, 2, 5] gives 8 comparisons and 6 shifts, [4, 3, 2, 1] gives 6 and 6, [1, 2, 3, 4] gives 3 and 0;
- the formulas n(n - 1)/2 and n - 1 for n = 100;
- merge sort moves equal n log2 n for powers of two.
