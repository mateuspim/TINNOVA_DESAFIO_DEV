import pytest
from bubble_sort import bubble_sort


def test_bubble_sort():
    arr = [64, 34, 25, 12, 22, 11, 90]
    sorted_arr = [11, 12, 22, 25, 34, 64, 90]
    bubble_sort(arr)
    assert arr == sorted_arr


def test_bubble_sort_empty_list():
    arr = []
    bubble_sort(arr)
    assert arr == []


def test_bubble_sort_already_sorted_list():
    arr = [1, 2, 3, 4, 5]
    bubble_sort(arr)
    assert arr == [1, 2, 3, 4, 5]


def test_bubble_sort_reversed_list():
    arr = [5, 4, 3, 2, 1]
    sorted_arr = [1, 2, 3, 4, 5]
    bubble_sort(arr)
    assert arr == sorted_arr
