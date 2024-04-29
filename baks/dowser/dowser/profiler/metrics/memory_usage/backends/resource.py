import time
import resource

from typing import Callable, Any
from toolz import compose, curry
from functools import wraps
from dowser.common import Report, session_context
from dowser.logger import get_logger
from dowser.core import build_parallelized_profiler
from dowser.profiler.context import profiler_context
from dowser.profiler.types import Metadata
from ..types import MemoryUsageRecord


def to_memory_usage_record(resource_usage: resource.struct_rusage) -> MemoryUsageRecord:
    timestamp = time.time()

    return timestamp, float(resource_usage.ru_maxrss)


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
def profile_memory_usage(
    report: Report,
    metadata: Metadata,
    function: Callable,
) -> Callable:
    logger = get_logger()
    logger.info(
        f'Setting up resource memory usage profiler for function "{metadata.get("function_path")}"'
    )

    pid = session_context.pid
    precision = profiler_context.memory_usage_precision

    metadata = {
        **metadata,
        "backend": "resource",
        "precision": precision,
        "unit": "kb",
    }

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug(
            f"Profiling memory usage of PID {pid} with precision of {precision}s"
        )
        hooked_function, get_memory_usage_log = resource_profiler(
            function,
            precision,
        )

        result = hooked_function(*args, **kwargs)
        memory_usage_log = get_memory_usage_log()
        logger.debug(f"Amount of collected profile records: {len(memory_usage_log)}")
        logger.debug(f"Sample record: {memory_usage_log[0]}")

        report.add_log("memory_usage", memory_usage_log, metadata)

        return result

    return wrapper


__all__ = ["profile_memory_usage"]
