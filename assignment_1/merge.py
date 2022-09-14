from typing import Union


def merge(left: Union[list, tuple], right: Union[list, tuple]) -> \
        Union[list, tuple]:
    """
    The function merges two sorted lists or tuples into a new list or
    tuple, that contains items of both original collections combined
    in sorted order
    :param left: first sorted collection
    :param right: second sorted collection
    :return: a resulting sorted collection
    """
    result = []
    left_iterator, right_iterator = iter(left), iter(right)
    left_item, right_item = next(left_iterator, []), next(right_iterator, [])
    while len(result) < len(left) + len(right):
        if left_item and right_item:
            if left_item <= right_item:
                result.append(left_item)
                left_item = next(left_iterator, [])
            else:
                result.append(right_item)
                right_item = next(right_iterator, [])
        else:
            if left_item:
                result.append(left_item)
                left_item = next(left_iterator, [])
            if right_item:
                result.append(right_item)
                right_item = next(right_iterator, [])

    return tuple(result) if isinstance(left, tuple) and \
        isinstance(right, tuple) else result


if __name__ == '__main__':
    assert merge([1, 2, 7], [3]) == [1, 2, 3, 7]
    assert merge((3, 15), (7, 8)) == (3, 7, 8, 15)
    assert merge([1, 2, 7, 9, 11, 42], [3, 5]) == [1, 2, 3, 5, 7, 9, 11, 42]
    assert merge(['a', 'c'], ['b', 'd', 'e', 'f', 'g']) == ['a', 'b', 'c', 'd',
                                                            'e', 'f', 'g']
    assert merge((1, 2), (3, 5, 7)) == (1, 2, 3, 5, 7)
    assert merge((), (3, 5, 7)) == (3, 5, 7)
    assert merge([1, 2, 5], []) == [1, 2, 5]
