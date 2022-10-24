import logging

from page_ranker_app import settings


main_log_file = settings.LOG_DIR.joinpath(settings.LOG_FILE)

crawler_handler = logging.FileHandler(main_log_file, mode=settings.LOG_MODE)
crawler_formatter = logging.Formatter(settings.CRAWLER_FORMAT)
crawler_handler.setFormatter(crawler_formatter)

crawler_logger = logging.getLogger(settings.CRAWLER_LOGGER_NAME)
crawler_logger.setLevel(settings.CRAWLER_LOGGER_LEVEL)
crawler_logger.addHandler(crawler_handler)


if __name__ == "__main__":
    pass
