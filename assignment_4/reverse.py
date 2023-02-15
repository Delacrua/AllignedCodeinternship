def reverse_dict(data: dict[int: list[int]]) -> dict[int: list[int]]:
    """
    The function reverses dictionaries key-value pairs in a way that
    each number from the lists of values becomes a key, and keys of the
    original key-value pairs are put into lists of values for new keys
    :param data: given dict
    :return: reversed dict
    """
    rev_data = {}
    for key, values in data.items():
        for value in values:
            rev_data[value] = rev_data.get(value, [])
            rev_data[value].append(key)
    return rev_data


if __name__ == '__main__':
    initial = {2: [3, 5], 1: [1, 2], 5: [2]}
    assert reverse_dict(initial) == {3: [2], 5: [2], 1: [1], 2: [1, 5]}
    assert reverse_dict(initial) != {3: [2], 1: [1], 2: [1, 5]}
