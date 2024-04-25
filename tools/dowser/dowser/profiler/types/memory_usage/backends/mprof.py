from typing import Callable, Any
from functools import wraps
from toolz import compose
from toolz.curried import map
from memory_profiler import memory_usage
from dowser.logger import get_logger
from dowser.profiler.context import profiler_context
from ..types import MemoryUsageRecord


def to_memory_usage_record(mprof_result: tuple[float, float]) -> MemoryUsageRecord:
    memory_usage, timestamp = mprof_result
    unit = "mb"

    return memory_usage, timestamp, unit


to_memory_usage_log = compose(list, map(to_memory_usage_record))


def profile_memory_usage(function: Callable) -> Callable:
    logger = get_logger()
    logger.info(
        f'Setting up psutil memory usage profiler for function "{function.__name__}"'
    )

    pid = profiler_context.session_pid
    precision = profiler_context.memory_usage_precision

    @wraps(function)
    def profiled_function(*args, **kwargs) -> Any:
        logger.debug(
            f"Profiling memory usage of PID {pid} with precision of {precision}s"
        )

        mprof_result, result = memory_usage(
            (function, args, kwargs),
            interval=precision,
            retval=True,
            timestamps=True,
        )

        memory_usage_log = to_memory_usage_log(mprof_result)

        logger.debug(f"Amount of collected profile points: {len(memory_usage_log)}")
        logger.debug(f"Sample data point: {memory_usage_log[0]}")

        profiler_result = [(memory_usage, "MB") for memory_usage in memory_usage_log]

        return result

    return profiled_function


__all__ = ["profile_memory_usage"]
