import pytest
from vote_counter import VoteCounter


def test_valid_votes():
    """
    Test with valid vote counts.
    """
    counter = VoteCounter(
        total_electors=100, valid_votes=75, blank_votes=10, invalid_votes=15
    )
    assert counter.valid_vote_percentage == 75.00
    assert counter.blank_vote_percentage == 10.00
    assert counter.invalid_vote_percentage == 15.00


def test_zero_total_electors():
    """
    Test with zero total electors, which should raise a ValueError.
    """
    with pytest.raises(ValueError):
        VoteCounter(total_electors=0, valid_votes=75, blank_votes=10, invalid_votes=15)


def test_negative_valid_votes():
    """
    Test negative valid votes, which should raise a ValueError.
    """
    with pytest.raises(ValueError):
        VoteCounter(
            total_electors=100, valid_votes=-1, blank_votes=10, invalid_votes=15
        )


def test_negative_blank_votes():
    """
    Test negative blank votes, which should raise a ValueError.
    """
    with pytest.raises(ValueError):
        VoteCounter(
            total_electors=100, valid_votes=10, blank_votes=-1, invalid_votes=15
        )


def test_negative_invalid_votes():
    """
    Test negative invalid votes, which should raise a ValueError.
    """
    with pytest.raises(ValueError):
        VoteCounter(
            total_electors=100, valid_votes=10, blank_votes=10, invalid_votes=-1
        )
