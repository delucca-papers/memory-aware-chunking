from dowser.config import MemoryUsageBackend, MemoryUsageUnit
from dowser.common.types import TraceFunction
from .tracer import trace


__all__ = ["build_tracer"]


def build_tracer(
    enabled_backends: list[MemoryUsageBackend],
    unit: MemoryUsageUnit,
) -> TraceFunction:
    return trace
