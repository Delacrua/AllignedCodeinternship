def smart_function():
    """
    a decorator that saves the state of namespace for counter function
    :return: counter object
    """
    count = 0

    def counter():
        """
        a function that counts its calls
        :return:
        """
        nonlocal count
        count += 1
        return count
    return counter


if __name__ == '__main__':
    f = smart_function()
    for real_call_count in range(1, 5):
        assert f() == real_call_count
