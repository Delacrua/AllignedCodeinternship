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


if __name__ == '__main__':
    @memorize
    def fib(x):
        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            return fib(x - 1) + fib(x - 2)


    print(fib(x=10))
    print(fib(100))
    print(fib(x=100))
