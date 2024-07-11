"""
Classes and functions for logging.
"""


import logging
from datetime import datetime
import os

PATH_LOG = "log.log"


def get_custom_logger() -> logging.Logger:
    """
    Create a logger object to be used by other parts of the repository.
    :return:
    """
    level = logging.INFO

    # Create logger
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=PATH_LOG, level=level, format=log_format)
    logger = logging.getLogger("custom_logger")
    return logger
