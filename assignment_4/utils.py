import timeit

from functools import wraps
from typing import Callable, Any


def profile(func: Callable) -> Callable:
    """
    A decorator to wrap a function 'func' with a wrapper
    :param func: a function to wrap
    :return: a wrapped func
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        """
        a wrapper that adds measuring of time used for a wrapped
        function to operate and printing it to stdout

        :param args: positional arguments for the func
        :param kwargs: keyword arguments for the func
        :return: result of func call
        """
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        end = timeit.default_timer()
        print(f'Function {wrapper.__name__} took {(end - start):.5f} seconds '
              f'to operate')
        return result
    return wrapper


class timer:
    """
    a context manager for measuring of time used for a code block
    to operate and printing it to stdout
    """
    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = timeit.default_timer()
        print(f'Code block took {(self.end - self.start):.5f} seconds '
              f'to operate')


if __name__ == '__main__':
    print('----->decorator block<-----')

    @profile
    def some_function():
        return sum(range(1_000_000))

    result1 = some_function()
    print(result1)

    print('----->context manager block<-----')

    with timer():
        print(sum(range(1_000_000)))
