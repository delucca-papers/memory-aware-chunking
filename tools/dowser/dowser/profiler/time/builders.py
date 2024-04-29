from dowser.profiler.types import TraceHooks
from .tracer import on_call


__all__ = ["build_tracer"]


def build_trace_hooks() -> TraceHooks:
    return {
        "on_call": [on_call],
    }
