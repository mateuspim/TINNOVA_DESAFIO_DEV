def bubble_sort(v: list) -> list:
    """
    Function that sorts a given list of integers using the Bubble Sort algorithm

    Time Complexity:     O (n²)
    Space Complexity:    O (1)

    :param v: The list to sort.
    :type v: list
    :return: The sorted list.
    :rtype: list
    """
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


if __name__ == "__main__":
    v = [5, 3, 2, 4, 7, 1, 0, 6]
    print(f"Initial vector: v = {v} \nafter sorting: \tv = {bubble_sort(v)}")
