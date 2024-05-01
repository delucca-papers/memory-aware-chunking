from psutil import Process
from types import FrameType
from typing import Any, Tuple
from dowser.config import ProfilerMetric


__all__ = ["on_call", "on_return"]


def get_memory_usage(process: Process = Process()) -> Tuple[float, str]:
    unit = "b"
    memory_usage = process.memory_info().rss

    return ProfilerMetric.MEMORY_USAGE.value, float(memory_usage), unit


def on_call(_: FrameType, __: str, ___: Any) -> Tuple[str, float, str]:
    return get_memory_usage()


def on_return(_: FrameType, __: str, ___: Any) -> Tuple[str, float, str]:
    return get_memory_usage()
