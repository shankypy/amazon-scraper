import logging
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler
from logging import Formatter
import sys
from amazon_scraper.settings import LOG_DIR

amazon_scraper_logger = None


def get_logger(logger_name, log_dir):

    logger = logging.getLogger(logger_name)

    file_formatter = Formatter(
        '%(levelname)s | %(asctime)s | %(name)s | %(message)s | %(pathname)s:%(lineno)d'
    )
    time_rotating_handler = TimedRotatingFileHandler(filename='{0}/{1}.log'.format(log_dir, logger_name),
                                                     when="midnight", encoding='utf-8')
    time_rotating_handler.suffix = "%Y-%m-%d"
    time_rotating_handler.setFormatter(file_formatter)

    if not logger.handlers:

        stream_handler = StreamHandler(stream=sys.stdout)
        echo_formatter = Formatter('[%(levelname)s][%(name)s][in %(filename)s:%(lineno)d] %(message)s')
        stream_handler.setFormatter(echo_formatter)

        logger.addHandler(time_rotating_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(logging.DEBUG)

    return logger


if amazon_scraper_logger is None:
    amazon_scraper_logger = get_logger('amazon_scraper_logger', LOG_DIR)
