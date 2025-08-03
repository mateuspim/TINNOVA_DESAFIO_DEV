# Exercise 03: Factorial

## Problem Description

This exercise implements a `Factorial` algorithm in Python.

## Project Structure

```
.
├── factorial.py
└── tests/
    └── test_factorial.py
```

## Factorial

The `factorial()` function implements the Factorial algorithm. It takes a integer as input and returns its factorial value.


### Function

```python
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Number must be non-negative")

    n_factored = 1
    for i in range(1, n + 1):
        n_factored *= i

    return n_factored
```

- **Parameters:**
  - `n`: The number to calculate the factorial for.

## How to run

### Prerequisites

You must have python3 and `pytest` installed. If you don't have `pytest`, it can be installed via pip using the following command:

```bash
pip install pytest
```

### Running the tests

To run tests for the `Factorial` method, execute the following command:

```bash
pytest tests/factorial.py -v
# or simply
pytest -v
```

The parameter `-v` (verbose) will show more information about the tests being executed.

### Executing an example (Optional)

You can execute the `factorial.py` file directly to see a basic usage example of the factorial algorithm:

```bash
python factorial.py