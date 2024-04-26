import time

from typing import Callable, Any
from functools import wraps
from toolz import curry
from dowser.common import Report
from dowser.logger import get_logger
from dowser.profiler.types import Metadata
from .types import TimeLog


def to_time_log(start_time: float, end_time: float) -> TimeLog:
    execution_time = end_time - start_time
    return [
        ("START", start_time),
        ("END", end_time),
        ("EXECUTION_TIME", execution_time),
    ]


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
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()

        time_log = to_time_log(start_time, end_time)
        logger.debug(f"Amount of collected profile records: {len(time_log)}")
        logger.debug(f"Sample record: {time_log[0]}")
        logger.debug(f"Total execution time: {time_log[-1][1]}s")

        report.add_log("time", time_log, metadata)

        return result

    return wrapper


__all__ = ["profile_time"]
