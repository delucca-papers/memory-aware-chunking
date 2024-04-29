from dowser.config import Config
from dowser.common.synchronization import lazy
from dowser.common.logger import logger
from .tracers import start_tracer, stop_tracer
from .handlers import execute_file
from .builders import build_trace_hooks


__all__ = ["run_profiler"]


def run_profiler(config: Config) -> None:
    logger.info("Starting profiler execution")

    trace_hooks = build_trace_hooks(
        config.profiler.enabled_metrics,
        config.profiler.memory_usage.enabled_backends,
    )
    lazy_start_tracer = lazy(start_tracer)(**trace_hooks)

    execute_file(
        config.profiler.filepath,
        config.profiler.args,
        config.profiler.kwargs,
        before=lazy_start_tracer,
        after=stop_tracer,
    )
