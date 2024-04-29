from dowser.common.types import TraceFunction
from .tracer import trace


__all__ = ["build_tracer"]


def build_tracer() -> TraceFunction:
    return trace
