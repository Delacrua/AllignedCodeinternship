import random


def _find_last_digit(odd_digits: list[int], even_digits: list[int]) -> int:
    """
    Helper function for counting the corresponding last digit of a card
    number using Luhn's algorithm
    :param odd_digits: a list of integers
    :param even_digits: a list of integers
    :return: the corresponding last
    digit of a card number
    """
    total = 0
    for digit in (*odd_digits, *even_digits):
        while digit:
            total += digit % 10
            digit //= 10
    last_digit = (10 - (total % 10)) % 10
    return last_digit


def check_card_number(card_number: int) -> bool:
    """
    The function checks if given card number is correct based on Luhn's
    algorithm
    :param card_number: card number
    :return: True if number
    correct, else False
    """
    if not (isinstance(card_number, int) and len(str(card_number)) == 16):
        return False
    check_digit = None
    odd_digits, even_digits = [], []
    flag = None
    while card_number:
        last_digit = card_number % 10
        card_number //= 10
        if flag is None:
            check_digit = last_digit
            flag = 'odd'
        elif flag == 'odd':
            odd_digits.append(last_digit * 2)
            flag = 'even'
        else:
            even_digits.append(last_digit)
            flag = 'odd'
    checksum = _find_last_digit(odd_digits, even_digits)
    return checksum == check_digit


def check_card_number_str(card_number: str) -> bool:
    """
    The function checks if given card number is correct based on Luhn's
    algorithm
    :param card_number: card number in string format
    :return: True
    if number correct, else False
    """
    if not (card_number.strip().isdigit() and len(card_number.strip()) == 16):
        return False
    digits = [int(digit) for digit in card_number.strip()]
    check_digit = digits[-1]
    odd_digits = [digit * 2 for digit in digits[-2::-2]]
    even_digits = digits[-3::-2]
    checksum = _find_last_digit(odd_digits, even_digits)
    return checksum == check_digit


def generate_card_number(system: str = 'visa'):
    """
    The function generates possible card numbers using Luhn's algorithm for
    two systems - Visa and Mastercard
    :param system: card system specification, either "visa" or "mastercard"
    :return: valid card number
    for given system
    """
    digits = []
    if system.lower() == 'visa':
        digits.append(4)
    elif system.lower() == 'mastercard':
        digits.append(5)
    else:
        return f'function got incorrect argument: {system}' \
               f'Argument must be either "visa" or "mastercard"'
    for _ in range(14):
        digits.append(random.randint(0, 9))
    odd_digits = [digit * 2 for digit in digits[-1::-2]]
    even_digits = digits[-2::-2]
    last_digit = _find_last_digit(odd_digits, even_digits)
    digits.append(last_digit)
    return int(''.join(map(str, digits)))


if __name__ == '__main__':
    assert check_card_number(5082337440657928)  # valid Mastercard
    assert not check_card_number(4601496706376197)  # invalid Visa
    assert not check_card_number(46014967063761978)  # invalid 17 dig
    assert not check_card_number_str('4601496706376197 ')  # invalid Visa
    assert not check_card_number_str('46014967063761976')  # invalid 17 ch
    assert check_card_number_str('5082337440657928')  # valid Mastercard
    assert check_card_number_str('5082337440657829 ')  # valid Mastercard
    assert check_card_number(generate_card_number('visa'))
    assert check_card_number(generate_card_number('mastercard'))

