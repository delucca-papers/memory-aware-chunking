from dowser.common.logger import logger
from dowser.profiler.types import TraceHooks
from .tracers import start_tracer, stop_tracer


__all__ = ["before", "after"]


def before(
    trace_hooks: TraceHooks,
    socket_path: str,
    depth: int = 10,
) -> None:
    logger.info("Running instrumentation before hooks")
    start_tracer(socket_path, depth, **trace_hooks)


def after() -> None:
    logger.info("Running instrumentation after hooks")
    stop_tracer()
