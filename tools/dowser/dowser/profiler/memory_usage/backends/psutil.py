from psutil import Process
from dowser.common.synchronization import passthrough
from dowser.profiler.types import CapturedTrace


__all__ = ["before", "on_call", "on_return", "after"]


def get_memory_usage(process: Process = Process()) -> float:
    memory_usage = process.memory_info().rss

    return float(memory_usage)


def capture_trace(*_) -> CapturedTrace:
    memory_usage = get_memory_usage()
    return "psutil_memory_usage", memory_usage


before = passthrough
after = passthrough
on_call = capture_trace
on_return = capture_trace
