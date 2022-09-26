from typing import Union, Tuple


def index(data_string: str,
          numbers: Union[int, Tuple[int, ...]],
          k: int = 5,
          ) -> tuple[int, list[int]]:
    """
    The function takes a string of digits of an integer and a number
    or a sequence of numbers and searches for all occurrences of those
    numbers in string returning a tuple that contains total number
    of occurrences of all searched numbers in the string and a list
    of first k sorted indices of those occurrences (counting that first
    elements of the string index is 1)
    :param data_string: a string of digits
    :param numbers: numbers to search
    :param k: limiter of output indices
    :return: number of occurrences and list of indices of occurrences
    """
    def _find_number(string: str, num: int, res_list: list) -> None:
        """
        Helper function for searching of all occurrences of a number
        in a string that stores indices of those occurrences (counting
        that first elements of the string index is 1)
        :param string: a string of digits
        :param num: number to search
        :param res_list: a resulting list of occurrences
        :return: None
        """
        pointer = 0
        while True:
            try:
                res_list.append(string.index(str(num), pointer) + 1)
                pointer = string.index(str(num), pointer) + len(str(num))
            except ValueError:
                break

    result = []
    if isinstance(numbers, int):
        _find_number(data_string, numbers, result)
    else:
        for number in numbers:
            _find_number(data_string, number, result)

    return len(result), sorted(result)[:k]


if __name__ == '__main__':
    assert (1, [1]) == index('123', 1)
    assert (13, [1, 1, 2]) == index('1212122222', (1, 2, 12), 3)
