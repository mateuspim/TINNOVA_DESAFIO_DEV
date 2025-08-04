# Exercise 04: Multiples of 3 or 5

## Problem Description

This exercise implements a `Multiples of 3 or 5` algorithm in Python.

## Project Structure

```
.
├── multiples.py
└── tests/
    └── test_multiples.py
```

## Multiples

The `multiples()` function implements the Multiples algorithm. It takes a integer as input and returns all multiples of 3 or 5 up to that number.


### Function

```python
def multiples(n: int) -> int:
    if n < 3:
        raise ValueError("Value should be greater or equal to 3")

    result = 0
    for i in range(3, n):
        if i % 3 == 0 or i % 5 == 0:
            result += i

    return result
```

- **Parameters:**
  - `n`: The number to calculate the muliples up to.

## How to run

### Prerequisites

You must have python3 and `pytest` installed. If you don't have `pytest`, it can be installed via pip using the following command:

```bash
pip install pytest
```

### Running the tests

To run tests for the `Multiples` method, execute the following command:

```bash
pytest tests/test_multiples.py -v
# or simply
pytest -v
```

The parameter `-v` (verbose) will show more information about the tests being executed.

### Executing an example (Optional)

You can execute the `multiples.py` file directly to see a basic usage example of the multiples algorithm:

```bash
python multiples.py