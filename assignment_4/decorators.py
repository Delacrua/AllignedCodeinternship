from functools import wraps


def memorize(func):
    """
    a decorator with a dictionary used to memoize func calls to prevent
    recalculating of previously calculated calls
    :param func: a function to wrap
    :return: wrapped function
    """
    mem_dict = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        a wrapper used to memoize func calls to prevent recalculating of
        previously calculated calls
        :param args: positional arguments for the func
        :param kwargs: keyword arguments for the func
        :return: result of func call
        """

        kwargs_values = []
        for key in sorted(kwargs):
            kwargs_values.append(kwargs[key])
        kwargs_values = tuple(kwargs_values)
        if (args, kwargs_values) not in mem_dict:
            mem_dict[(args, kwargs_values)] = func(*args, **kwargs)
        return mem_dict[(args, kwargs_values)]

    return wrapper


def convolve(k: int):
    """
    a decorator with passing of an argument 'k' to implement k times
    function convolution
    :param k: a number of convolutions
    :return: a decorated func
    """
    assert isinstance(k, int) and k > 0

    def decorator(func):
        """
        A decorator to wrap a function 'func' with a wrapper
        :param func: a function to wrap
        :return: a wrapped func
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            a wrapper for convolving given func k times
            :param args: positional arguments for the func
            :param kwargs: keyword arguments for the func
            :return: wrapped func
            """
            result = func(*args, **kwargs)
            for i in range(k - 1):
                result = func(result)
            return result
        return wrapper
    return decorator


if __name__ == '__main__':
    print('----->memorize block<-----')

    @memorize
    def fib(number):
        if number == 0:
            return 0
        elif number == 1:
            return 1
        else:
            return fib(number - 1) + fib(number - 2)

    print(fib(number=10))
    print(fib(100))
    print(fib(number=100))

    print('----->convolve block<-----')

    @convolve(3)
    def f(some_argument):
        return 2 * some_argument
    x = 1
    assert f(x) == 2 * (2 * (2 * x))  # f(f(f(x)))

    @convolve(1)
    def f2(some_argument):
        return 2 * some_argument
    x = 1
    assert f2(x) == 2 * x  # f(x)

