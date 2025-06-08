import logging
import time
from functools import wraps

from utils.logger import setup_logger

logger = setup_logger()


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} executed in {end - start:.4f}s")
        return result
    return wrapper
