import time

from typing import Callable, NamedTuple, Any
from toolz import compose, curry
from functools import wraps
from psutil import Process
from dowser.common import Report, session_context
from dowser.logger import get_logger
from dowser.core import build_parallelized_profiler
from dowser.profiler.context import profiler_context
from dowser.profiler.types import Metadata
from ..types import MemoryUsageRecord


def to_memory_usage_record(memory_info: NamedTuple) -> MemoryUsageRecord:
    timestamp = time.time()

    return timestamp, float(memory_info.rss)


def get_memory_info(process: Process) -> NamedTuple:
    return process.memory_info()


psutil_profiler = build_parallelized_profiler(
    compose(
        to_memory_usage_record,
        get_memory_info,
    )
)


@curry
def profile_memory_usage(
    report: Report,
    metadata: Metadata,
    function: Callable,
) -> Callable:
    logger = get_logger()
    logger.info(
        f'Setting up psutil memory usage profiler for function "{function.__name__}"'
    )

    pid = session_context.pid
    precision = profiler_context.memory_usage_precision
    process = Process(pid=pid)

    metadata = {
        **metadata,
        "backend": "psutil",
        "precision": precision,
        "unit": "b",
    }

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug(
            f"Profiling memory usage of PID {pid} with precision of {precision}s"
        )
        hooked_function, get_memory_usage_log = psutil_profiler(
            function,
            precision,
            process,
        )

        result = hooked_function(*args, **kwargs)
        memory_usage_log = get_memory_usage_log()
        logger.debug(f"Amount of collected profile records: {len(memory_usage_log)}")
        logger.debug(f"Sample record: {memory_usage_log[0]}")

        report.add_log("memory_usage", memory_usage_log, metadata)

        return result

    return wrapper


__all__ = ["profile_memory_usage"]
