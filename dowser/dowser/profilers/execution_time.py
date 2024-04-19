import time

from typing import Callable, Any
from functools import wraps
from ..core.config import config
from ..core.logging import get_logger


def profile(config: dict = config) -> Callable:
    logger = get_logger()

    def decorator(function: Callable) -> Callable:
        logger.info(
            f'Setting up execution time profiler for function "{function.__name__}"'
        )

        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            function_results = function(*args, **kwargs)
            end_time = time.time()

            execution_time = end_time - start_time

            logger.debug(f"Profiler results: {execution_time} seconds")

            return function_results

        return wrapper

    return decorator


__all__ = ["profile"]
