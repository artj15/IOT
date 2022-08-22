import logging
import os

from misc import config

logger = logging.getLogger(__name__)
CONFIG_ENV_KEY = 'SRVC_CONFIG'


def main_with_parses(entry_point):
    try:
        config_path = os.environ[CONFIG_ENV_KEY]
        conf = config.read_config(config_path)
    except:
        logger.error(f'Configuration file path not provided at environment [{CONFIG_ENV_KEY}]')
        return None
    if conf is None:
        logger.error(f'Configuration file at path {config_path} not found')
    else:
        return entry_point(conf)
