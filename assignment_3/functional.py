from collections import deque
from typing import Iterable, Any, Generator


def flatten(sequence: list[Any]) -> Generator:
    """
    The function flattens nested iterables (except for strings) without
    using recursion
    :param sequence: a sequence with nested iterables
    :return: generator of sequence contents
    """
    queue = deque()
    for item in sequence:
        if not isinstance(item, Iterable) or isinstance(item, str):
            yield item
        else:
            queue.extend(item)
            while queue:
                item = queue.popleft()
                if not isinstance(item, Iterable) or isinstance(item, str):
                    yield item
                else:
                    queue.extendleft(item)


if __name__ == '__main__':
    expected = [1, 2, 0, 1, 1, 2, 1, 'ab']
    actual = flatten([1, 2, range(2), [[], [1], [[2]]], (x for x in [1]), 'ab']
                     )
    assert expected == list(actual)
