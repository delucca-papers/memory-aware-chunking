import tracemalloc

from dowser.profiler.types import CapturedTrace


__all__ = ["before", "on_call", "on_return", "on_sample", "after"]


def get_memory_usage() -> float:
    memory_usage = tracemalloc.get_traced_memory()[0]

    return float(memory_usage)


def capture_trace(*_) -> CapturedTrace:
    memory_usage = get_memory_usage()
    return "tracemalloc_memory_usage", memory_usage


before = tracemalloc.start
after = tracemalloc.stop
on_call = capture_trace
on_return = capture_trace
on_sample = capture_trace
