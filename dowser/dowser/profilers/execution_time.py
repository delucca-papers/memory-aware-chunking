import time

from typing import Callable, Any
from functools import wraps
from ..core import get_logger


def profile(function: Callable) -> Callable:
    logger = get_logger()
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


__all__ = ["profile"]
