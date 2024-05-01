import tracemalloc

from types import FrameType
from typing import Any, Tuple
from dowser.config import ProfilerMetric


__all__ = ["before", "on_call", "on_return", "after"]


def get_memory_usage() -> Tuple[float, str]:
    unit = "b"
    memory_usage = tracemalloc.get_traced_memory()[0]

    return ProfilerMetric.MEMORY_USAGE.value, float(memory_usage), unit


def before() -> None:
    tracemalloc.start()


def on_call(_: FrameType, __: str, ___: Any) -> Tuple[str, float, str]:
    return get_memory_usage()


def on_return(_: FrameType, __: str, ___: Any) -> Tuple[str, float, str]:
    return get_memory_usage()


def after() -> None:
    tracemalloc.stop()
