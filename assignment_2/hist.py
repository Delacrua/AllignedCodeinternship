from typing import Union


def distribute(collection: list[Union[int, float]], number: int):
    """
    The function calculates the histogram of the distribution of numbers
    in the given collection, splitting it into the specified number of
    segments
    :param collection: the given collection
    :param number: the specified number of segments
    :return: a list of distribution of elements in segments
    """
    minimum, maximum = min(collection), max(collection)
    interval = (maximum - minimum) / number
    result = [0 for _ in range(number)]
    for num in collection:
        index = (num - minimum) / interval
        if index < number:
            result[int(index)] += 1
        else:
            result[-1] += 1
    return result


if __name__ == '__main__':
    assert distribute([1.25, 1, 2, 1.75], 2) == [2, 2]
    assert distribute([1.25, 1, 2, 1.75, 1.45], 2) == [3, 2]
    assert distribute([1.25, 1, 2, 1.75, 1.45, 1.50], 2) == [3, 3]
