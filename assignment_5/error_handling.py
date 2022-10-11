import logging
import random
import sys
import traceback

from time import sleep
from typing import Optional, Union, Type


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
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = None
            func_delay = delay

            if tries is None:
                while True:
                    try:
                        result = func(*args, **kwargs)
                    except exc_type:
                        sleep(func_delay)
                        func_delay *= backoff
                    else:
                        break
            elif isinstance(tries, int):
                if tries <= 0:
                    raise ValueError('tries argument must be a positive integer')
                else:
                    for _ in range(tries - 1):
                        try:
                            result = func(*args, **kwargs)
                        except exc_type:
                            sleep(func_delay)
                            func_delay *= backoff
                        else:
                            break
            if not result:
                try:
                    result = func(*args, **kwargs)
                except exc_type as exc:
                    if re_raise:
                        raise exc
                    if log_traceback:
                        logger.error(traceback.format_exc())

            return result

        return wrapper
    return decorator


if __name__ == '__main__':
    # @handle_error(re_raise=False)
    # def some_function():
    #     x = 1 / 0  # ZeroDivisionError
    #
    # some_function()
    # print(1)  # line will be executed as exception is suppressed


    # @handle_error(re_raise=False, exc_type=KeyError)
    # def some_function():
    #     x = 1 / 0  # ZeroDivisionError
    # some_function()
    # print(1)  # line won ’t be executed as exception is re - raised

    # @handle_error(re_raise=False, log_traceback=False)
    # def some_function():
    #     x = 1 / 0  # ZeroDivisionError
    # some_function()
    # print(1)  # line will be executed as exception is suppressed


    @handle_error(re_raise=True, tries=3, delay=0.5, backoff=2)
    def some_function():
        if random.random() < 0.75:
            x = 1 / 0  # ZeroDivisionError

    some_function()
