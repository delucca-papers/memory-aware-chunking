from typing import List, Tuple, Dict, Literal, Callable
from dowser.config import (
    MemoryUsageBackend,
    ProfilerMetric,
    FunctionParameter,
    ProfilerInstrumentationConfig,
)
from dowser.common.transformers import deep_merge
from dowser.common.logger import logger
from .metrics.memory_usage import build_trace_hooks as build_memory_usage_trace_hooks
from .metrics.time import build_trace_hooks as build_time_trace_hooks
from .strategies.instrumentation.builders import (
    build_executor_hooks as build_instrumentation_executor_hooks,
)
from .types import TraceHooks, ExecutorHooks


__all__ = [
    "build_trace_hooks",
    "build_executor_hooks",
    "build_metadata",
]

def build_trace_hooks(
    enabled_metrics: List[ProfilerMetric],
    enabled_memory_usage_backends: List[MemoryUsageBackend],
) -> TraceHooks:
    memory_usage_hooks = (
        build_memory_usage_trace_hooks(enabled_memory_usage_backends)
        if ProfilerMetric.MEMORY_USAGE in enabled_metrics
        else {}
    )
    time_hooks = (
        build_time_trace_hooks() if ProfilerMetric.TIME in enabled_metrics else {}
    )
    return deep_merge(memory_usage_hooks, time_hooks, append=True)


def build_executor_hooks(
    trace_hooks: TraceHooks,
    instrumentation_config: ProfilerInstrumentationConfig,
    on_data: Callable,
    strategy: Literal["instrumentation"] = "instrumentation",
) -> ExecutorHooks:
    logger.debug(f"Building executor hooks using strategy: {strategy}")

    strategy_builders = {
        "instrumentation": build_instrumentation_executor_hooks(instrumentation_config),
    }

    builder = strategy_builders[strategy]

    return builder(trace_hooks, on_data)


def build_metadata(
    signature: List[FunctionParameter], args: Tuple, kwargs: Dict
) -> Dict:
    entrypoint_args_names = [param.name for param in signature]
    entrypoint_args = {entrypoint_args_names[i]: str(arg) for i, arg in enumerate(args)}
    entrypoint_kwargs = {k: str(v) for k, v in kwargs.items()}

    return {
        **{
            f"entrypoint_{arg_name}": arg_value
            for arg_name, arg_value in entrypoint_args.items()
        },
        **{
            f"entrypoint_{arg_name}": arg_value
            for arg_name, arg_value in entrypoint_kwargs.items()
        },
        "kernel_memory_usage_unit": "kb",
        "psutil_memory_usage_unit": "b",
        "resource_memory_usage_unit": "kb",
        "tracemalloc_memory_usage_unit": "b",
        "unix_timestamp_unit": "ms",
    }
