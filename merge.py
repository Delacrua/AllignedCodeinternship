from typing import Union


def merge(left: Union[list, tuple], right: Union[list, tuple]) -> \
        Union[list, tuple]:
    """
    The function merges two sorted lists or tuples into a new list or
    tuple, that contains items of both original
    collections combined in sorted order
    :param left: first sorted collection
    :param right: second sorted collection
    :return: a resulting sorted collection
    """
    result = []
    if len(left) == 0:
        result = [item for item in right]
    elif len(right) == 0:
        result = [item for item in left]
    else:
        left_iterator, right_iterator = iter(left), iter(right)
        left_item, right_item = next(left_iterator), next(right_iterator)

        while True:
            if left_item <= right_item:
                result.append(left_item)
                try:
                    left_item = next(left_iterator)
                except StopIteration:
                    result.append(right_item)
                    break
            else:
                result.append(right_item)
                try:
                    right_item = next(right_iterator)
                except StopIteration:
                    result.append(left_item)
                    break
        for item in left_iterator:
            result.append(item)
        for item in right_iterator:
            result.append(item)

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
