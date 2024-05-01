from types import FrameType
from typing import Any, Tuple
from io import TextIOWrapper
from dowser.config import ProfilerMetric
from dowser.common.file_handling import get_line_with_keyword, go_to_pointer
from dowser.common.synchronization import passthrough


__all__ = ["before", "on_call", "on_return", "after"]


before = passthrough
after = passthrough


def get_memory_usage(
    status_file: TextIOWrapper = open("/proc/self/status", "r"),
) -> Tuple[float, str]:
    file_content = go_to_pointer(0, status_file)
    status_line = get_line_with_keyword("VmRSS", file_content)
    memory_usage, unit = status_line.split(":")[1].split()

    return ProfilerMetric.MEMORY_USAGE.value, float(memory_usage), unit


def on_call(_: FrameType, __: str, ___: Any) -> Tuple[str, float, str]:
    return get_memory_usage()


def on_return(_: FrameType, __: str, ___: Any) -> Tuple[str, float, str]:
    return get_memory_usage()
