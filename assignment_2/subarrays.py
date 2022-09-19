def get_subarrays_count(integers: list[int], number: int) -> int:
    """
    The function gets count of all continuous segments in the list of
    integers, the sum of which is equal to the given number
    :param integers: the list of integers
    :param number: the given number
    :return: count of all segments that satisfy task's conditions
    """
    count = 0
    for left in range(len(integers)):
        for right in range(left, len(integers)):
            if sum(integers[left:right + 1]) == number:
                count += 1
    return count


if __name__ == '__main__':
    assert get_subarrays_count([0, 1, 0], 1) == 4
    assert get_subarrays_count([1, 1, 1], 2) == 2
    assert get_subarrays_count([1, 0, 1, 1], 2) == 3
