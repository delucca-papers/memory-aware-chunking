from toolz import curry
from dowser.config import ProfilerInstrumentationConfig
from dowser.common.synchronization import lazy
from dowser.profiler.types import TraceHooks, ExecutorHooks
from dowser.profiler.buffer import Buffer
from .tracers import start_tracer, stop_tracer


__all__ = ["build_executor_hooks"]


@curry
def build_executor_hooks(
    config: ProfilerInstrumentationConfig,
    buffer: Buffer,
    trace_hooks: TraceHooks,
) -> ExecutorHooks:
    return {
        "before": lazy(start_tracer)(
            depth=config.depth,
            buffer=buffer,
            **trace_hooks,
        ),
        "after": lazy(stop_tracer)(buffer),
    }
