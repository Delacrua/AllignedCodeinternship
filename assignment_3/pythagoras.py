import math

from typing import Generator


def get_pythagoras_triples(number: int) -> Generator:
    """
    The function returns a generator of all pythagoras triples for
    a given number
    :param number: a given number
    :return: a generator of pythagoras triples
    """
    return ((a, b, int(math.sqrt(a ** 2 + b ** 2)))
            for b in range(number)
            for a in range(1, b)
            if math.sqrt(a ** 2 + b ** 2) % 1 == 0)


if __name__ == '__main__':
    assert list(get_pythagoras_triples(12)) == [(3, 4, 5), (6, 8, 10)]

