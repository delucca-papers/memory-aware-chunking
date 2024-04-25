from typing import Callable
from toolz import compose, identity
from dowser.logger import get_logger
from dowser.profiler.context import profiler_context
from .backends import kernel, mprof, psutil, resource, tracemalloc


def profile_memory_usage(function: Callable) -> Callable:
    logger = get_logger()
    logger.info(f'Setting up memory usage profiler for function "{function.__name__}"')

    enabled_backends = profiler_context.memory_usage_enabled_backends
    logger.debug(f"Enabled memory usage backends: {enabled_backends}")

    return compose(
        (kernel.profile_memory_usage if "kernel" in enabled_backends else identity),
        (mprof.profile_memory_usage if "mprof" in enabled_backends else identity),
        (psutil.profile_memory_usage if "psutil" in enabled_backends else identity),
        (resource.profile_memory_usage if "resource" in enabled_backends else identity),
        (
            tracemalloc.profile_memory_usage
            if "tracemalloc" in enabled_backends
            else identity
        ),
    )(function)


__all__ = ["profile_memory_usage"]
