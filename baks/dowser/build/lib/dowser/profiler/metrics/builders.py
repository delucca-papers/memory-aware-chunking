from typing import Callable
from toolz import compose, identity, curry
from dowser.logger import get_logger
from dowser.common import Report
from dowser.profiler.context import profiler_context
from dowser.profiler.types import Metadata
from .memory_usage import profile_memory_usage
from .time import profile_time


@curry
def build_enabled_profilers(
    report: Report,
    metadata: Metadata,
    function: Callable,
) -> Callable:
    logger = get_logger()

    enabled_profilers = profiler_context.enabled_profilers
    logger.debug(f"Enabled profilers: {enabled_profilers}")

    return compose(
        (
            profile_memory_usage(report, metadata)
            if "memory_usage" in enabled_profilers
            else identity
        ),
        (profile_time(report, metadata) if "time" in enabled_profilers else identity),
    )(function)


__all__ = ["build_enabled_profilers"]
