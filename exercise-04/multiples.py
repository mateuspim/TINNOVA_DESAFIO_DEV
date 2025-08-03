def multiples(n: int) -> int:
    """
    A function that sums up all values that are multiples of 3 or 5 until the given value.

    Time Complexity:  O (n)
    Space Complexity: O (1)

    :param n: The upper limit for calculating multiples.
    :type n: int
    :return: The sum of multiples of 3 and/or 5 up to but not including `n`.
    :rtype: int
    """
    if n < 3:
        raise ValueError("Value should be greater or equal to 3")

    result = 0
    for i in range(3, n):
        if i % 3 == 0 or i % 5 == 0:
            result += i

    return result


if __name__ == "__main__":
    num = 10
    print(f"The sum of multiples of 3 or 5 under {num} is {multiples(num)}")
