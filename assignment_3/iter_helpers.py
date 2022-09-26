from collections.abc import Iterable


def transpose(iterable: Iterable[Iterable[int]]) -> list[list[int]]:
    """
    The function performs a matrix transposition and returns transposed
    matrix in a form of a list of lists
    :param iterable: a given matrix
    :return: a transposed matrix
    """
    return list(map(list, (zip(*iterable))))


if __name__ == '__main__':
    expected = [[1, 2], [-1, 3]]
    actual = transpose([[1, -1], [2, 3]])
    assert expected == list(map(list, actual))
