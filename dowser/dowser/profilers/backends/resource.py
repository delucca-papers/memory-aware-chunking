import time
import resource

from typing import Callable
from threading import Event
from queue import Queue
from toolz import compose
from ...core import threaded_wrapper, get_logger
from ..types import MemoryUsageWrapper


def profile_memory_usage(event: Event, queue: Queue, precision) -> None:
    logger = get_logger()
    logger.info(
        f"Profiling memory usage with resource backend with precision of {precision}s"
    )

    while not event.is_set():
        current_memory_usage = get_memory_usage(resource.RUSAGE_SELF)

        queue.put((current_memory_usage, "kB"))
        time.sleep(precision)


get_memory_usage = compose(
    lambda ru: ru.ru_maxrss,
    resource.getrusage,
)


###


def wrapper(function: Callable, precision: float) -> MemoryUsageWrapper:
    return threaded_wrapper(function, profile_memory_usage, precision)


__all__ = ["wrapper"]
