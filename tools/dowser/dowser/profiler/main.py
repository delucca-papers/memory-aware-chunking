from typing import Callable
from functools import wraps
from dowser.logger import get_logger
from .types import build_enabled_profilers


def profile(function: Callable):
    logger = get_logger()
    logger.info(f'Setting up profilers for function "{function.__name__}"')

    with_enabled_profilers = build_enabled_profilers()
    profiled_function = with_enabled_profilers(function)

    @wraps(function)
    def wrapper(*args, **kwargs):
        logger.info(f'Profiling function "{function.__name__}"')
        return profiled_function(*args, **kwargs)

    return wrapper


__all__ = ["profile"]
