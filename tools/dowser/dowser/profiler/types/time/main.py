from typing import Callable
from dowser.logger import get_logger


def profile_time(function: Callable) -> Callable:
    logger = get_logger()
    logger.info(f'Setting up time profiler for function "{function.__name__}"')

    return function


__all__ = ["profile_time"]
