def get_primes(number: int) -> list[int]:
    """
    The function returns a list of prime numbers not greater than the
    given number
    :param number: the given number
    :return: a list of prime numbers
    """
    return [num for num in range(2, number + 1) if
            all(num % div != 0 for div in range(2, int(num ** 0.5) + 1))]


if __name__ == '__main__':
    assert [2, 3, 5, 7, 11] == sorted(get_primes(11))
