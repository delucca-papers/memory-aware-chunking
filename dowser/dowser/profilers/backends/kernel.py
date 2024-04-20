import os
import time

from typing import Callable
from threading import Event
from queue import Queue
from toolz import compose
from ...core import threaded_wrapper, go_to_pointer, get_line_with_keyword, get_logger
from ..types import MemoryUsageWrapper


def profile_memory_usage(
    event: Event,
    queue: Queue,
    precision,
    pid: int = os.getpid(),
) -> None:
    logger = get_logger()
    logger.info(
        f"Profiling memory usage with kernel backend with precision of {precision}s"
    )

    with open(f"/proc/{pid}/status", "r") as status_file:
        while not event.is_set():
            current_memory_usage, unit = seek_memory_usage(status_file)

            queue.put((current_memory_usage, unit))
            time.sleep(precision)


def get_vm_size_value_and_unit(line: str) -> tuple[float, str]:
    memory_usage, unit = line.split(":")[1].split()
    return float(memory_usage), unit


seek_memory_usage = compose(
    get_vm_size_value_and_unit,
    get_line_with_keyword("VmSize"),
    go_to_pointer(0),
)


###


def wrapper(function: Callable, precision: float) -> MemoryUsageWrapper:
    return threaded_wrapper(function, profile_memory_usage, precision)


__all__ = ["wrapper"]
