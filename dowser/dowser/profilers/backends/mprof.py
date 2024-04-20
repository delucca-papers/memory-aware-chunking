from typing import Callable
from memory_profiler import memory_usage
from functools import wraps
from ...core import get_logger
from ..types import MemoryUsageWrapper, MemoryUsageWrappedResult


def wrapper(function: Callable, precision: float) -> MemoryUsageWrapper:
    logger = get_logger()
    logger.info("Using mprof thread as wrapper")

    @wraps(function)
    def profiled_function(*args, **kwargs) -> MemoryUsageWrappedResult:
        memory_usage_log, result = memory_usage(
            (function, args, kwargs),
            interval=precision,
            retval=True,
        )

        profiler_result = [(memory_usage, "MB") for memory_usage in memory_usage_log]

        return profiler_result, result

    return profiled_function


__all__ = ["wrapper"]
