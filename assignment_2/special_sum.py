def calculate_special_sum(number: int) -> int:
    """
    Еhe function returns the sum of the following expression:
    1**2 * 2 + 2**2 * 3 + ... + (n − 1)**2 * n,
    where n is the given number
    :param number: the given number
    :return: sum of the expression
    """
    return sum((num - 1) ** 2 * num for num in range(2, number + 1))


if __name__ == '__main__':
    assert calculate_special_sum(3) == 14
    assert calculate_special_sum(4) == 50
    assert calculate_special_sum(1) == 0
