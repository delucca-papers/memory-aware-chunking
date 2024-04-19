import os
import time

from typing import Callable
from threading import Event
from queue import Queue
from toolz import compose
from psutil import Process
from ...core.threading import threaded_wrapper
from ...core.logging import get_logger
from ..types import MemoryUsageWrapper


def profile_memory_usage(
    event: Event,
    queue: Queue,
    precision,
    pid: int = os.getpid(),
) -> None:
    logger = get_logger()
    logger.info(
        f"Profiling memory usage with psutil backend with precision of {precision}s"
    )

    process = Process(pid=pid)

    while not event.is_set():
        current_memory_usage = get_memory_usage(process)

        queue.put((current_memory_usage, "b"))
        time.sleep(precision)


get_memory_usage = compose(
    lambda mi: mi.rss,
    lambda p: p.memory_info(),
)


###


def wrapper(function: Callable, precision: float) -> MemoryUsageWrapper:
    return threaded_wrapper(function, profile_memory_usage, precision)


__all__ = ["wrapper"]
