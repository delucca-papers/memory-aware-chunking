import time
import resource

from typing import Callable, Any
from toolz import compose, curry
from functools import wraps
from dowser.common import get_function_path
from dowser.logger import get_logger
from dowser.core import build_parallelized_profiler
from dowser.profiler.context import profiler_context
from ....report import ProfilerReport
from ..types import MemoryUsageRecord


def to_memory_usage_record(resource_usage: resource.struct_rusage) -> MemoryUsageRecord:
    timestamp = time.time()
    unit = "kb"

    return timestamp, float(resource_usage.ru_maxrss), unit


def get_resource_usage() -> resource.struct_rusage:
    return resource.getrusage(resource.RUSAGE_SELF)


resource_profiler = build_parallelized_profiler(
    compose(
        to_memory_usage_record,
        get_resource_usage,
    ),
    strategy="thread",
)


@curry
def profile_memory_usage(report: ProfilerReport, function: Callable) -> Callable:
    logger = get_logger()
    logger.info(
        f'Setting up resource memory usage profiler for function "{function.__name__}"'
    )

    pid = profiler_context.session_pid
    precision = profiler_context.memory_usage_precision

    metadata = {
        "backend": "resource",
        "precision": precision,
        "function_path": get_function_path(function),
    }

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug(
            f"Profiling memory usage of PID {pid} with precision of {precision}s"
        )
        hooked_function, get_memory_usage_profile = resource_profiler(
            function,
            precision,
        )

        result = hooked_function(*args, **kwargs)
        memory_usage_profile = get_memory_usage_profile()
        logger.debug(f"Amount of collected profile points: {len(memory_usage_profile)}")
        logger.debug(f"Sample data point: {memory_usage_profile[0]}")

        report.add_profile("memory_usage", memory_usage_profile, metadata)

        return result

    return wrapper


__all__ = ["profile_memory_usage"]
