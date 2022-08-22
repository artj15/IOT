import os
from logging.config import fileConfig


def logger_conf():
    fileConfig(os.getenv('LOG_CONFIG'))
