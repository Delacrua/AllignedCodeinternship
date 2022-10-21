import functools
import logging
import time
import timeit
import traceback

from typing import Optional, Union, Type, Callable, Any

from page_ranker import settings


def handle_errors(
        logger: logging.Logger,
        re_raise: bool = settings.EXCEPTION_RE_RAISE,
        log_traceback: bool = settings.LOG_ERRORS,
        exc_type: Union[Type[Exception], tuple[Type[Exception]]] = settings.EXCEPTION_TYPE,
        tries: Optional[int] = settings.MAX_RETRIES,
        delay: Union[int, float] = settings.RETRY_DELAY,
) -> Callable:
    """
    A decorator used to handle and log exceptions
    :param logger: a logger object for logging exceptions
    :param re_raise: shows if Exceptions listed in exc_type will be
    reraised
    :param log_traceback: shows if traceback of Exceptions listed in
    exc_type will be logged
    :param exc_type: an Exception type or a tuple of Exception types
    :param tries: a number of tries to call decorated function before
    raising Exception
    :param delay: delay between tries in seconds
    :return: decorated function object
    """
    def decorator(func: Callable) -> Callable:
        """
        A decorator wraps given func with a wrapper
        :param func: given func
        :return: wrapped func
        """
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            """
            a wrapper that implements the logics of handle_error
            decorator, according to arguments given
            :param args: any number of positional arguments
            :param kwargs: any number of keyword arguments
            :return:
            """
            logger.info(f'Calling {func.__name__} with arguments: {args}')
            func_delay = delay
            func_tries = tries if type(tries) == int and tries > 0 else settings.MAX_RETRIES

            while func_tries:
                func_tries -= 1
                try:
                    return func(*args, **kwargs)
                except exc_type as exc:
                    if func_tries:
                        logger.error(f'Error: {exc} Retrying call of {func.__name__} with arguments: {args}')
                        time.sleep(func_delay)
                    else:
                        if log_traceback:
                            logger.error(traceback.format_exc())
                        if re_raise:
                            raise exc
        return wrapper
    return decorator


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
