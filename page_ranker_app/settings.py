import logging
import os
import pathlib


BASE_DIR = pathlib.Path(__file__).resolve().parent


class NotSet:
    pass


NOT_SET = NotSet()


# ----> inverters.py defaults <-----
# Threading inverter
THREADS_INVERTING = 100

# Multiprocessing inverter
PROCESSES_INVERTING = 20

# ----> crawlers.py defaults <-----
REQUEST_TIMEOUT = 5


# ----> page_ranker.py defaults <-----
THREADS_SCRAPPING = 100  # 1 worker does 1 request per second
MAX_REQUESTS_PER_SECOND = 200


# ----> loggers.py defaults <-----
LOG_DIR = BASE_DIR
LOG_FILE = "page_ranker.log"
LOG_MODE = 'w'

# Crawler logger
CRAWLER_LOGGER_NAME = 'Crawler'
CRAWLER_LOGGER_LEVEL = logging.INFO
CRAWLER_FORMAT = "%(name)s %(levelname)s %(asctime)s - %(message)s"


# ----> utils.py defaults <-----
# handle_errors
EXCEPTION_RE_RAISE = True
LOG_ERRORS = True
EXCEPTION_TYPE = Exception
MAX_RETRIES = 2
RETRY_DELAY = 1


if __name__ == '__main__':
    pass
