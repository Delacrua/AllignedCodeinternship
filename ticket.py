def get_nearest_lucky_ticket(ticket_number: int) -> int:
    """
    The function returns the nearest lucky ticket number to the given ticket number (according to the task number is
    lucky if sum of its first three digits is equal to sum of its last three digits)
    :param ticket_number: given ticket number
    :return: nearest lucky ticket number
    """
    def _is_lucky(number: int) -> bool:
        """
        Helper function to find if a six-digit number is lucky in terms of the task
        :param number: given number
        :return: True if number is lucky, else False
        """
        digits = [int(digit) for digit in str(number)]
        return sum(digits[:3]) == sum(digits[3:])

    if _is_lucky(ticket_number):
        return ticket_number
    elif ticket_number == 100_000:  # set this as a unique case as a lower number will be 5-digit
        return 100_001
    else:
        higher_number = ticket_number + 1
        while not _is_lucky(higher_number):
            higher_number += 1
        lower_number = ticket_number - 1
        while not _is_lucky(lower_number):
            lower_number -= 1

        return lower_number if ticket_number - lower_number <= higher_number - ticket_number else higher_number


if __name__ == '__main__':
    assert get_nearest_lucky_ticket(111_111) == 111_111
    assert get_nearest_lucky_ticket(123_322) == 123_321
    assert get_nearest_lucky_ticket(123_320) == 123_321
    assert get_nearest_lucky_ticket(333_999) != 333_900
    assert get_nearest_lucky_ticket(333_999) == 334_019
    assert get_nearest_lucky_ticket(100_000) == 100_001
    assert get_nearest_lucky_ticket(999_999) == 999_999
    assert get_nearest_lucky_ticket(999_998) == 999_999
