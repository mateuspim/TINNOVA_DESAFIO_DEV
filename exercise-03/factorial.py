def factorial(n: int) -> int:
    """
    A function that calculates the factorial of a number.

    :param n int: The number to calculate the factorial for.
    :return: The factorial of the given number.
    """
    if n < 0:
        raise ValueError("Number must be non-negative")

    n_factored = 1
    for i in range(1, n + 1):
        n_factored *= i

    return n_factored


if __name__ == "__main__":
    print(f"Factorial of {0} is {factorial(0)}")
    print(f"Factorial of {1} is {factorial(1)}")
    print(f"Factorial of {2} is {factorial(2)}")
    print(f"Factorial of {3} is {factorial(3)}")
    print(f"Factorial of {4} is {factorial(4)}")
    print(f"Factorial of {5} is {factorial(5)}")
    print(f"Factorial of {6} is {factorial(6)}")
