import random

from dowser.config import Config
from dowser.common.logger import logger
from .tracers import build_tracer, stop_tracer
from .handlers import execute_file
from .builders import build_trace_hooks


__all__ = ["run_profiler"]


def run_profiler(config: Config) -> None:
    logger.info("Starting profiler execution")

    trace_hooks = build_trace_hooks(
        config.profiler.enabled_metrics,
        config.profiler.memory_usage.enabled_backends,
    )
    start_tracer, traces = build_tracer(**trace_hooks)

    logger.info(f'Starting profiler execution for "{config.profiler.filepath}"')
    logger.debug(f"Enabled hooks: {trace_hooks.keys()}")
    logger.debug(f"Enabled metrics: {config.profiler.enabled_metrics}")
    logger.debug(f"Using args: {config.profiler.args}")
    logger.debug(f"Using kwargs: {config.profiler.kwargs}")

    execute_file(
        config.profiler.filepath,
        config.profiler.args,
        config.profiler.kwargs,
        before=start_tracer,
        after=stop_tracer,
    )

    amount_of_traces = len(traces)
    sample_trace_index = random.randint(0, amount_of_traces - 1)

    logger.info("Profiler execution finished")
    logger.info(f"Amount of collected traces: {amount_of_traces}")
    logger.debug(f"Sample trace: {traces[sample_trace_index]}")
