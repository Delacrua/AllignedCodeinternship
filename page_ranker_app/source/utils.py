import functools
import logging
import math
import time
import timeit
import traceback
import matplotlib.pyplot as plt

from typing import Optional, Union, Type, Callable, Any, Dict

from page_ranker_app import settings

Exc_variants = Union[Type[Exception], tuple[Type[Exception]]]


def handle_errors(
    logger: logging.Logger,
    re_raise: bool = settings.EXCEPTION_RE_RAISE,
    log_traceback: bool = settings.LOG_ERRORS,
    exc_type: Exc_variants = settings.EXCEPTION_TYPE,
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
            logger.info(f"Calling {func.__name__} with arguments: {args}")
            func_delay = delay
            func_tries = (
                tries
                if type(tries) == int and tries > 0
                else settings.MAX_RETRIES
            )

            while func_tries:
                func_tries -= 1
                try:
                    return func(*args, **kwargs)
                except exc_type as exc:
                    if func_tries:
                        logger.error(
                            f"Error: {exc} Retrying call of {func.__name__} with arguments: {args}"
                        )
                        time.sleep(func_delay)
                    else:
                        if log_traceback:
                            logger.error(traceback.format_exc())
                        if re_raise:
                            raise exc

        return wrapper

    return decorator


def count_distribution(
    collection: Dict[str, int],
    number: int = settings.BINS_NUMBER,
) -> Dict[str, int]:
    """
    The function calculates the distribution of numbers in the given
    dictionary where values are integers (similar to collections.Counter),
    splitting it into the specified number of segments

    :param collection: the given collection
    :param number: the specified number of segments
    :return: a dict of distribution of elements in segments
    """
    values = [math.log(value) for value in collection.values()]
    minimum, maximum = min(values), max(values)
    interval = (maximum - minimum) / number
    result = [0 for _ in range(number)]
    for num in values:
        index = (num - minimum) / interval
        result[min(int(index), number - 1)] += 1
    keys = [
        f"{round(interval * n, 1)}-{round(interval * (n + 1), 1)}"
        for n in range(number)
    ]

    return dict(zip(keys, result))


def print_hist_and_plot_combined(freq_counter: Dict[str, int]) -> None:
    """
    A function that prints a combined figure of a histogram and a plot
    of distribution of values from a dictionary

    :param freq_counter: a dictionary with distribution of values
    :return: None
    """
    plt.figure(figsize=(16, 6))
    plt.subplot(121)
    plt.bar(
        freq_counter.keys(),
        freq_counter.values(),
        log=True,
        color="blue",
        edgecolor="black",
    )
    plt.xlabel("Log(Page Rank)")
    plt.ylabel("Number of pages")
    plt.subplot(122)
    plt.plot(freq_counter.keys(), freq_counter.values())
    plt.xlabel("Log(Page Rank)")
    plt.ylabel("Number of pages")
    plt.suptitle("Distribution of log(Page Rank)")
    plt.show()


class timer:
    """
    a context manager for measuring of time used for a code block
    to operate and printing it to stdout
    """
    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = timeit.default_timer()
        print(
            f"Code block took {(self.end - self.start):.5f} seconds "
            f"to operate"
        )
