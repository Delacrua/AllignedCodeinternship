def get_subarrays_count(integers: list[int], number: int) -> int:
    """
    The function gets count of all continuous segments in the list of
    integers, the sum of which is equal to the given number
    :param integers: the list of integers
    :param number: the given number
    :return: count of all segments that satisfy task's conditions
    """
    count = 0
    length = len(integers)
    sums = [[0 for _ in range(length + 1)] for _ in range(length + 1)]
    for row in range(1, length + 1):
        for col in range(row, length + 1):
            if row == col == 1:
                sums[row][col] = integers[0]
            else:
                sums[row][col] = sums[row][col - 1] + integers[col - 1]
            if sums[row][col] == number:
                count += 1
    return count


if __name__ == '__main__':
    assert get_subarrays_count([0, 1, 0], 1) == 4
    assert get_subarrays_count([1, 1, 1], 2) == 2
    assert get_subarrays_count([1, 0, 1, 1], 2) == 3

