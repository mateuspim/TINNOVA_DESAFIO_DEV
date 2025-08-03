# Exercise 01: Vote Tally

## Problem Description

This exercise implements a `VoteCounter` class in Python to manage the counting of votes (valid, blank, and invalid) in relation to the total number of electors.

## Project Structure

```
.
├── vote_counter.py
└── tests/
    └── test_vote_counter.py
```

## VoteCounter Class

The `VoteCounter` class calculates the percentages of valid, blank, and invalid votes.

### Constructor

```python
def __init__(
    self,
    total_electors: int,
    valid_votes: int,
    blank_votes: int,
    invalid_votes: int,
):
```

- **Parameters:**

  - `total_electors`: The total number of electors.
  - `valid_votes`: The number of valid votes.
  - `blank_votes`: The number of blank votes.
  - `invalid_votes`: The number of invalid votes.

- **Raises:**
  - `ValueError`: If `total_electors` is less than or equal to zero, or if any vote count is negative.

### Properties

### valid_vote_percentage

```python
@property
def valid_vote_percentage(self) -> float:
```

Calculates the percentage of valid votes.

- **Returns:** The percentage of valid votes as a float.

### blank_vote_percentage

```python
@property
def blank_vote_percentage(self) -> float:
```

Calculates the percentage of blank votes.

- **Returns:** The percentage of blank votes as a float.

### invalid_vote_percentage

```python
@property
def invalid_vote_percentage(self) -> float:
```

Calculates the percentage of invalid votes.

- **Returns:** The percentage of invalid votes as a float.

## How to run

### Prerequisites

You must have python3 and `pytest` installed. If you don't have `pytest`, it can be installed via pip using the following command:

```bash
pip install pytest
```

### Running the tests

To run tests for the `VoteCounter` class, execute the following command:

```bash
pytest tests/test_vote_counter.py -v
# or simply
pytest -v
```

The parameter `-v` (verbose) will show more information about the tests being executed.

### Executing an example (Optional)

You can execute the `vote_counter.py` file directly to see a basic usage example of the class:

```bash
python vote_counter.py
```
