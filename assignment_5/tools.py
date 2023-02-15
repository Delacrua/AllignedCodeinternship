def merge_json(*args: dict) -> dict:
    """
    a function to merge arbitrary number of dictionaries according
    to the rules given in task
    :param args: an arbitrary number of dictionaries
    :return: a dictionary
    """
    result = {}
    for dictionary in args:
        for key, value in dictionary.items():
            if key not in result:
                result[key] = value
            elif type(value) != type(result[key]):
                raise ValueError(f'Types of values for key {key} '
                                 f'do not match in merged dictionaries')
            elif isinstance(value, list):
                result[key].extend(value)
            elif isinstance(value, dict):
                result[key] = merge_json(result[key], value)
            else:
                result[key] = value
    return result


if __name__ == '__main__':
    lhs = {'s': True,
           'x': [2, 3],
           'y': {'a': 1, 'b': 2, 'c': [11]}
           }
    rhs = {'s': False,
           'x': [3, 4],
           'y': {'a': 3, 'c': [12]}
           }
    expected = {'s': False,
                'x': [2, 3, 3, 4],
                'y': {'a': 3, 'b': 2, 'c': [11, 12]}
                }
    assert expected == merge_json(lhs, rhs)
