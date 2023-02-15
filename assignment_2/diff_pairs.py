from typing import Union


def get_pairs_count(collection: Union[list, tuple], number: int) -> int:
    """
    The function returns a count of unique pairs in collection which
    difference is equal to the given number
    :param collection: a collection of integers
    :param number: the given number
    :return: a count of unique pairs
    """
    count = 0
    result = {}
    for item in collection:
        result[item] = result.get(item, 0) + 1
    if number == 0:
        count = sum(1 for value in result.values() if value > 1)
    else:
        for key in result:
            if result.get(key - number, False):
                count += 1
    return count


if __name__ == '__main__':
    assert get_pairs_count([5, 4, 3, 2, 1], 1) == 4
    assert get_pairs_count([1, 2, 3, 4, 5], 1) == 4
    assert get_pairs_count((1, 3, 1, 5, 4), 0) == 1
    assert get_pairs_count((1, 3, 1, 5, 4, 1), 0) == 1
    assert get_pairs_count((1, 3, 1, 5, 4, 1, 3), 0) == 2
