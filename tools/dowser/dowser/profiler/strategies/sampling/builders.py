from toolz import curry
from dowser.profiler.types import TraceHooks, ExecutorHooks
from dowser.profiler.buffer import Buffer
from dowser.config.profiler import SamplingConfig
from .samplers import create_samplers


__all__ = ["build_executor_hooks"]


@curry
def build_executor_hooks(
    config: SamplingConfig,
    buffer: Buffer,
    trace_hooks: TraceHooks,
) -> ExecutorHooks:
    start_sampler, stop_sampler = create_samplers(buffer, trace_hooks, config.precision)

    return {
        "before": start_sampler,
        "after": stop_sampler,
    }
