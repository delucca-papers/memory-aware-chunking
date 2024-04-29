import time

from typing import Callable, Any
from functools import wraps
from toolz import curry
from dowser.common import Report
from dowser.logger import get_logger
from dowser.profiler.types import Metadata
from .tracer import start_tracer, stop_tracer


@curry
def profile_time(report: Report, metadata: Metadata, function: Callable) -> Callable:
    logger = get_logger()
    logger.info(f'Setting up time profiler for function "{function.__name__}"')

    metadata = {
        **metadata,
        "unit": "seconds",
    }

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        time_log = start_tracer()
        result = function(*args, **kwargs)
        stop_tracer()

        total_execution_time = time_log[-1][0] - time_log[0][0]

        logger.debug(f"Amount of collected profile records: {len(time_log)}")
        logger.debug(f"Sample record: {time_log[0]}")
        logger.debug(f"Total execution time: {total_execution_time}s")

        report.add_log("time", time_log, metadata)

        return result

    return wrapper


__all__ = ["profile_time"]
