from dowser.config import Config, ProfilerMetric
from dowser.common.synchronization import lazy, passthrough
from dowser.common.logger import logger
from dowser.common.introspection import get_function_path
from .tracers import start_tracer, stop_tracer
from .handlers import execute_file
from .memory_usage.builders import build_tracer as build_memory_usage_tracer
from .time.builders import build_tracer as build_time_tracer


__all__ = ["run_profiler"]


def run_profiler(config: Config) -> None:
    logger.info("Starting profiler execution")

    memory_usage_trace = (
        build_memory_usage_tracer(
            config.profiler.memory_usage.enabled_backends,
            config.profiler.memory_usage.unit,
        )
        if ProfilerMetric.MEMORY_USAGE in config.profiler.enabled_metrics
        else passthrough
    )
    time_trace = (
        build_time_tracer()
        if ProfilerMetric.TIME in config.profiler.enabled_metrics
        else passthrough
    )
    lazy_start_tracer = lazy(start_tracer)(memory_usage_trace, time_trace)

    logger.debug(
        f'Memory usage tracer in use: "{get_function_path(memory_usage_trace)}"'
    )
    logger.debug(f'Time tracer in use: "{get_function_path(time_trace)}"')

    execute_file(
        config.profiler.filepath,
        config.profiler.args,
        config.profiler.kwargs,
        before=lazy_start_tracer,
        after=stop_tracer,
    )
