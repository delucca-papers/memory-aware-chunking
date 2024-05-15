import resource

from dowser.common.synchronization import passthrough
from dowser.profiler.types import CapturedTrace


__all__ = ["before", "on_call", "on_return", "after"]


def get_memory_usage() -> float:
    memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    return float(memory_usage)


def capture_trace(*_) -> CapturedTrace:
    memory_usage = get_memory_usage()
    return "resource_memory_usage", memory_usage


before = passthrough
after = passthrough
on_call = capture_trace
on_return = capture_trace
