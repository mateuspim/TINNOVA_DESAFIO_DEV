import pytest
from multiples import multiples


def test_multiples_10():
    assert multiples(10) == 23, "The sum of multiples of 3 or 5 up to 10 should be 23"


def test_multiples_20():
    assert multiples(20) == 78, "The sum of multiples of 3 or 5 up to 20 should be 78"


def test_multiples_30():
    assert multiples(30) == 195, "The sum of multiples of 3 or 5 up to 30 should be 195"


def test_multiples_exception():
    with pytest.raises(ValueError):
        assert multiples(0)
