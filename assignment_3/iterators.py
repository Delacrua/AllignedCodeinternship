from typing import Iterable, Generator


def unique(sequence: Iterable) -> Generator:
    """
    The function takes an iterable and returns only unique elements of
    the iterable in initial order
    :param sequence: an iterable
    :return: a generator of unique elements of sequence
    """
    used = set()
    for item in sequence:
        if item not in used:
            used.add(item)
            yield item


if __name__ == '__main__':
    expected = [1, 2, 3]
    actual = unique([1, 2, 1, 3, 2])
    assert expected == list(actual)
