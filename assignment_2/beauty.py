def get_beauties(number: int) -> tuple[int, int]:
    """
    The function takes an integer and returns a tuple of two integers,
    which sum is equal to the original integer and which are both
    'beautiful' in terms of task
    Beauty in terms of task means that number is positive and doesn't
    contain '0' in it
    :param number:
    :return:
    """
    def _check_beauty(checked_num: int) -> bool:
        """
        Helper function to check if a number is beautiful in terms of
        the task
        :param checked_num: checked number
        :return: True if beautiful, else False
        """
        return checked_num > 0 and '0' not in f'{checked_num}'

    for num in range(1, number):
        if _check_beauty(num) and _check_beauty(number - num):
            return num, number - num


if __name__ == '__main__':
    assert get_beauties(13) == (1, 12)
    assert get_beauties(1010) == (11, 999)
    assert get_beauties(61) == (2, 59)
