from itertools import starmap
from typing import Optional, Iterable, Union

matrix = Iterable[Iterable[int]]
vector = Iterable[Union[int, float, str]]


def transpose(iterable: matrix) -> matrix:
    """
    The function performs a matrix transposition and returns transposed
    matrix in a form of a list of lists
    :param iterable: a given matrix
    :return: a transposed matrix
    """
    return list(map(list, (zip(*iterable))))


def scalar_product(vector_a: vector, vector_b: vector) -> Optional[int]:
    """
    The function returns a scalar product of two vectors using their
    coordinates in a plane
    :param vector_a: first vector
    :param vector_b: second vector
    :return: a scalar product of two vectors
    """
    try:
        vectors = [list(map(int, vector_a)), list(map(int, vector_b))]
    except ValueError:
        return None
    return sum(starmap(lambda x, y: x * y, vectors))


if __name__ == '__main__':
    # transpose block
    expected = [[1, 2], [-1, 3]]
    actual = transpose([[1, -1], [2, 3]])
    assert expected == list(map(list, actual))

    # scalar_product block
    expected = 1
    actual = scalar_product([1, '2'], [-1, 1])
    assert expected == actual
    actual = scalar_product([1, 'xyz'], [-1, 1])
    assert actual is None
