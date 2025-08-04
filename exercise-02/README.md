# Exercise 02: Bubble Sort

## Problem Description

This exercise implements a `Bubble Sort` algorithm in Python.

## Project Structure

```
.
├── bubble_sort.py
└── tests/
    └── test_bubble_sort.py
```

## Bubble Sort

The `bubble_sort()` function implements the Bubble Sort algorithm. It takes a list of integers as input and sorts it in ascending order using the bubble sort algorithm.


### Function

```python
def bubble_sort(v: list) -> list:
    if not v:
        return v

    length = len(v)

    for i in range(length - 1):
        swapped = False
        for j in range(length - i - 1):
            if v[j] > v[j + 1]:
                v[j], v[j + 1] = v[j + 1], v[j]
                swapped = True
        if not swapped:
            break

    return v
```

- **Parameters:**
  - `v`: The list of integers to be sorted.

## How to run

### Prerequisites

You must have python3 and `pytest` installed. If you don't have `pytest`, it can be installed via pip using the following command:

```bash
pip install pytest
```

### Running the tests

To run tests for the `BubbleSort` function, execute the following command:

```bash
pytest tests/bubble_sort.py -v
# or simply
pytest -v
```

The parameter `-v` (verbose) will show more information about the tests being executed.

### Executing an example (Optional)

You can execute the `bubble_sort.py` file directly to see a basic usage example of the sorting algorithm:

```bash
python bubble_sort.py