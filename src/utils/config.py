import yaml

from utils.logger import setup_logger

CONFIG = None

log = setup_logger()


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
            log.fatal(f"Exception occurred trying to load config: {exc}")

    return CONFIG
