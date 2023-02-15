import math

from itertools import combinations

from typing import Generator


def get_pythagoras_triples(number: int) -> Generator:
    """
    The function returns a generator of all pythagoras triples for
    a given number
    :param number: a given number
    :return: a generator of pythagoras triples
    """
    return (
        (a, b, int(math.sqrt(a ** 2 + b ** 2)))
        for a, b in combinations(range(1, number + 1), 2)
        if math.sqrt(a ** 2 + b ** 2) % 1 == 0
           and 1 <= int(math.sqrt(a ** 2 + b ** 2)) <= number
    )


if __name__ == '__main__':
    print(list(get_pythagoras_triples(12)))
    assert list(get_pythagoras_triples(12)) == [(3, 4, 5), (6, 8, 10)]

