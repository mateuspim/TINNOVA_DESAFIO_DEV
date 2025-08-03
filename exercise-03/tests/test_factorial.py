import pytest
from factorial import factorial


def test_factorial_0():
    assert factorial(0) == 1


def test_factorial_1():
    assert factorial(1) == 1


def test_factorial_2():
    assert factorial(2) == 2


def test_factorial_3():
    assert factorial(3) == 6


def test_factorial_4():
    assert factorial(4) == 24


def test_factorial_5():
    assert factorial(5) == 120


def test_factorial_6():
    assert factorial(6) == 720


def test_factorial_7():
    assert factorial(7) == 5040


def test_factorial_8():
    assert factorial(8) == 40320


def test_factorial_9():
    assert factorial(9) == 362880
