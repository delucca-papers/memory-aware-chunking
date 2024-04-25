from typing import Callable, Any
from functools import wraps
from toolz import compose, curry
from toolz.curried import map
from memory_profiler import memory_usage
from dowser.common import get_function_path
from dowser.logger import get_logger
from dowser.profiler.context import profiler_context
from ....report import ProfilerReport
from ..types import MemoryUsageRecord


def to_memory_usage_record(mprof_result: tuple[float, float]) -> MemoryUsageRecord:
    timestamp, memory_usage = mprof_result
    unit = "mb"

    return memory_usage, timestamp, unit


to_memory_usage_log = compose(list, map(to_memory_usage_record))


@curry
def profile_memory_usage(report: ProfilerReport, function: Callable) -> Callable:
    logger = get_logger()
    logger.info(
        f'Setting up mprof memory usage profiler for function "{function.__name__}"'
    )

    pid = profiler_context.session_pid
    precision = profiler_context.memory_usage_precision

    metadata = {
        "backend": "mprof",
        "precision": precision,
        "function_path": get_function_path(function),
    }

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

        report.add_profile("memory_usage", memory_usage_log, metadata)

        return result

    return profiled_function


__all__ = ["profile_memory_usage"]
