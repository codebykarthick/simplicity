import sys

import yaml

from utils.logger import setup_logger

CONFIG = None
logger = setup_logger()


def load_config():
    """Loads the config from YAML file and returns a Dictionary

    Returns:
        dict[str, Any]: The loaded config dictionary.
    """
    global CONFIG
    if CONFIG is None:
        try:
            with open("./config.yml") as stream:
                CONFIG = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.fatal(f"Exception occurred trying to load config: {exc}")
            sys.exit(1)

        logger.info(f"Loaded config file successfully: {CONFIG}")

    return CONFIG
