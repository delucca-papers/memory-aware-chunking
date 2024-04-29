import time
import tracemalloc

from typing import Callable, Any
from toolz import compose, curry
from functools import wraps
from dowser.common import Report, session_context
from dowser.logger import get_logger
from dowser.core import build_parallelized_profiler
from dowser.profiler.context import profiler_context
from dowser.profiler.types import Metadata
from ..types import MemoryUsageRecord


def to_memory_usage_record(traced_memory: tuple[int, int]) -> MemoryUsageRecord:
    timestamp = time.time()

    return timestamp, float(traced_memory[0])


def get_traced_memory() -> tuple[int, int]:
    return tracemalloc.get_traced_memory()


tracemalloc_profiler = build_parallelized_profiler(
    compose(
        to_memory_usage_record,
        get_traced_memory,
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
        f'Setting up tracemalloc memory usage profiler for function "{metadata.get("function_path")}"'
    )

    pid = session_context.pid
    precision = profiler_context.memory_usage_precision

    metadata = {
        **metadata,
        "backend": "tracemalloc",
        "precision": precision,
        "unit": "b",
    }

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug(
            f"Profiling memory usage of PID {pid} with precision of {precision}s"
        )
        tracemalloc.start()
        hooked_function, get_memory_usage_log = tracemalloc_profiler(
            function,
            precision,
        )

        result = hooked_function(*args, **kwargs)
        memory_usage_log = get_memory_usage_log()
        tracemalloc.stop()

        logger.debug(f"Amount of collected profile records: {len(memory_usage_log)}")
        logger.debug(f"Sample record: {memory_usage_log[0]}")

        report.add_log("memory_usage", memory_usage_log, metadata)

        return result

    return wrapper


__all__ = ["profile_memory_usage"]
