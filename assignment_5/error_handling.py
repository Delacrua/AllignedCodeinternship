import logging
import random
import sys
import traceback

from contextlib import contextmanager
from time import sleep
from typing import Optional, Union, Type, Callable

logger = logging
log_format = "%(levelname)s %(asctime)s - %(message)s"
logger.basicConfig(
    level=logging.ERROR,
    stream=sys.stdout,
    format=log_format,
    datefmt='%Y:%m:%d %H:%M:%S',
)


def handle_error(
        re_raise: bool = True,
        log_traceback: bool = True,
        exc_type: Union[Type[Exception], tuple[Type[Exception]]] = Exception,
        tries: Optional[int] = 1,
        delay: Union[int, float] = 0,
        backoff: int = 1,
) -> Callable:
    """

    :param re_raise: shows if Exceptions listed in exc_type will be
    reraised
    :param log_traceback: shows if traceback of Exceptions listed in
    exc_type will be logged
    :param exc_type: an Exception type or a tuple of Exception types
    :param tries: a number of tries to call decorated function before
    raising Exception
    :param delay: delay between tries in seconds
    :param backoff: a multiplier implied to delay after each try
    :return: decorated function object
    """
    def decorator(func: Callable) -> Callable:
        """
        A decorator wraps given func with a wrapper
        :param func: given func
        :return: wrapped func
        """
        def wrapper(*args, **kwargs):
            """
            a wrapper that implements the logics of handle_error
            decorator, according to arguments given
            :param args: any number of positional arguments
            :param kwargs: any number of keyword arguments
            :return:
            """
            result = None
            func_delay = delay
            func_tries = tries if tries else True

            if isinstance(func_tries, int) and func_tries < 0:
                raise ValueError('tries argument must be a positive '
                                 'integer')
            while func_tries:
                if type(func_tries) == int:
                    func_tries -= 1
                try:
                    result = func(*args, **kwargs)
                except exc_type as exc:
                    if func_tries:
                        sleep(func_delay)
                        func_delay *= backoff
                    else:
                        if log_traceback:
                            logger.error(traceback.format_exc())
                        if re_raise:
                            raise exc
                else:
                    break
            return result

        return wrapper
    return decorator


@contextmanager
def handle_error_context(
        re_raise: bool = True,
        log_traceback: bool = True,
        exc_type: Union[Type[Exception], tuple[Type[Exception]]] = Exception,
):
    try:
        yield
    except exc_type as exc:
        if log_traceback:
            logger.error(traceback.format_exc())
        if re_raise:
            raise exc


if __name__ == '__main__':
    print('----------->Decorator block<-------------')
    # # Example 1
    # @handle_error(re_raise=False)
    # def some_function():
    #     x = 1 / 0  # ZeroDivisionError
    # some_function()
    # print(1)  # line will be executed as exception is suppressed

    # # Example 2
    # @handle_error(re_raise=False, exc_type=KeyError)
    # def some_function():
    #     x = 1 / 0  # ZeroDivisionError
    # some_function()
    # print(1)  # line won ’t be executed as exception is re - raised

    # # Example 3
    # @handle_error(re_raise=False, log_traceback=False)
    # def some_function():
    #     x = 1 / 0  # ZeroDivisionError
    # some_function()
    # print(1)  # line will be executed as exception is suppressed

    # # Example 4
    # @handle_error(re_raise=True, tries=3, delay=0.5, backoff=2)
    # def some_function():
    #     if random.random() < 0.75:
    #         x = 1 / 0  # ZeroDivisionError
    # some_function()

    # # Example 5 (testing tries=None)
    # @handle_error(re_raise=True, tries=None, delay=0.5, backoff=2)
    # def some_function():
    #     if random.random() < 0.75:
    #         x = 1 / 0  # ZeroDivisionError
    # some_function()
    #
    print('----------->Context manager block<-------------')
    # # Example 1 - log traceback , reraise exception
    # with handle_error_context(
    #         log_traceback=True,
    #         exc_type=ValueError
    # ):
    #     raise ValueError()

    # # Example 2 - log traceback , don't reraise exception
    # with handle_error_context(
    #         log_traceback=True,
    #         exc_type=ValueError,
    #         re_raise=False
    # ):
    #     raise ValueError()
