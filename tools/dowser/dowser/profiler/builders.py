from typing import List
from dowser.config import MemoryUsageBackend, ProfilerMetric
from dowser.common.transformers import deep_merge
from .memory_usage import build_trace_hooks as build_memory_usage_trace_hooks
from .time import build_trace_hooks as build_time_trace_hooks
from .types import TraceHooks


__all__ = ["build_trace_hooks"]


def build_trace_hooks(
    enabled_metrics: List[ProfilerMetric],
    enabled_memory_usage_backends: List[MemoryUsageBackend],
) -> TraceHooks:
    memory_usage_trace_hooks = (
        build_memory_usage_trace_hooks(enabled_memory_usage_backends)
        if ProfilerMetric.MEMORY_USAGE in enabled_metrics
        else {}
    )
    time_trace_hooks = (
        build_time_trace_hooks() if ProfilerMetric.TIME in enabled_metrics else {}
    )

    return deep_merge(memory_usage_trace_hooks, time_trace_hooks, append=True)
