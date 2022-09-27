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


def flatten2(sequence: list[Any]) -> Generator:
    """
    The function flattens nested iterables (except for strings) without
    using recursion
    :param sequence: a sequence with nested iterables
    :return: generator of sequence contents
    """
    stack = deque()
    for item in sequence:
        if not isinstance(item, Iterable) or isinstance(item, str):
            yield item
        else:
            stack.append(item)
            while stack:
                popped = iter(stack.pop())
                for sub in popped:
                    if not isinstance(sub, Iterable) or isinstance(sub, str):
                        yield sub
                    else:
                        stack.append(popped)
                        stack.append(sub)
                        break


def flatten3(sequence: list[Any]) -> Generator:
    """
    The function flattens nested iterables (except for strings) without
    using recursion
    :param sequence: a sequence with nested iterables
    :return: generator of sequence contents
    """
    stack = deque()
    for item in sequence:
        stack.append(item)
        while stack:
            popped = stack.pop()
            if not isinstance(popped, Iterable) or isinstance(popped, str):
                yield popped
            else:
                popped = iter(popped)
                for sub in popped:
                    stack.append(popped)
                    stack.append(sub)
                    break


if __name__ == '__main__':
    expected = [1, 2, 0, 1, 1, 2, 1, 'ab']
    actual = flatten3([1, 2, range(2), [[], [1], [[2]]], (x for x in [1]), 'ab']
                     )
    assert expected == list(actual)
