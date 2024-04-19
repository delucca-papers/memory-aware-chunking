import time
import tracemalloc

from typing import Callable
from threading import Event
from queue import Queue
from toolz import compose, first
from ...core.threading import threaded_wrapper
from ...core.logging import get_logger
from ..types import MemoryUsageWrapper


def profile_memory_usage(event: Event, queue: Queue, precision) -> None:
    logger = get_logger()
    logger.info(
        f"Profiling memory usage with tracemalloc backend with precision of {precision}s"
    )

    tracemalloc.start()

    while not event.is_set():
        current_memory_usage = get_memory_usage()

        queue.put((current_memory_usage, "b"))
        time.sleep(precision)

    tracemalloc.stop()


get_memory_usage = compose(
    first,
    tracemalloc.get_traced_memory,
)


###


def wrapper(function: Callable, precision: float) -> MemoryUsageWrapper:
    return threaded_wrapper(function, profile_memory_usage, precision)


__all__ = ["wrapper"]
