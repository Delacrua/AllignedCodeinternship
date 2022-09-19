from typing import Union


def get_pairs_count(collection: Union[list, tuple], number: int) -> int:
    """
    The function returns a count of unique pars in collection which
    difference is equal to the given number
    :param collection: a collection of integers
    :param number: the given number
    :return: a count of unique pars
    """
    result = set()
    for i, item in enumerate(collection):
        if item - number in collection[:i] + collection[i + 1:]:
            result.add(frozenset((item, item - number)))
    return len(result)


if __name__ == '__main__':
    assert get_pairs_count([5, 4, 3, 2, 1], 1) == 4
    assert get_pairs_count((1, 3, 1, 5, 4), 0) == 1
