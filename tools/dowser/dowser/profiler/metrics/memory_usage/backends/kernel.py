import time

from typing import Callable, Any
from toolz import compose, curry
from functools import wraps
from dowser.common import get_function_path, Report
from dowser.logger import get_logger
from dowser.core import (
    get_line_with_keyword,
    go_to_pointer,
    build_parallelized_profiler,
)
from dowser.profiler.context import profiler_context
from ..types import MemoryUsageRecord


def to_memory_usage_record(line: str) -> MemoryUsageRecord:
    memory_usage, _ = line.split(":")[1].split()
    timestamp = time.time()

    return timestamp, float(memory_usage)


kernel_profiler = build_parallelized_profiler(
    compose(
        to_memory_usage_record,
        get_line_with_keyword("VmSize"),
        go_to_pointer(0),
    )
)


@curry
def profile_memory_usage(report: Report, function: Callable) -> Callable:
    logger = get_logger()
    logger.info(
        f'Setting up kernel memory usage profiler for function "{function.__name__}"'
    )

    pid = profiler_context.session_pid
    precision = profiler_context.memory_usage_precision
    status_file = open(f"/proc/{pid}/status", "r")

    metadata = {
        "backend": "kernel",
        "precision": precision,
        "function_path": get_function_path(function),
        "unit": "kb",
    }

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug(
            f"Profiling memory usage of PID {pid} with precision of {precision}s"
        )
        hooked_function, get_memory_usage_log = kernel_profiler(
            function,
            precision,
            status_file,
        )

        result = hooked_function(*args, **kwargs)
        memory_usage_log = get_memory_usage_log()
        logger.debug(f"Amount of collected profile records: {len(memory_usage_log)}")
        logger.debug(f"Sample record: {memory_usage_log[0]}")

        report.add_log("memory_usage", memory_usage_log, metadata)

        return result

    return wrapper


__all__ = ["profile_memory_usage"]
