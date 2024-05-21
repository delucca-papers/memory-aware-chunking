import importlib

from dowser.config import MemoryUsageBackend
from dowser.common.logger import logger
from dowser.profiler.types import TraceHooks


__all__ = ["build_tracer"]


def build_trace_hooks(enabled_backends: MemoryUsageBackend) -> TraceHooks:
    logger.info(f'Enabled memory usage backends: "{enabled_backends}"')

    hooks = {
        "before": [],
        "on_call": [],
        "on_return": [],
        "on_sample": [],
        "after": [],
    }

    for backend in enabled_backends:
        backend_name = backend.value.lower()

        logger.debug(f'Loading backend: "{backend_name}"')
        backend_module = importlib.import_module(
            f"dowser.profiler.metrics.memory_usage.backends.{backend_name}"
        )

        if not backend_module:
            raise ImportError(f'Backend "{backend_name}" not found')

        logger.debug(f'Loaded backend: "{backend_module}"')

        for hook_name in hooks.keys():
            logger.debug(f'Checking if backend has "{hook_name}" function')

            if not hasattr(backend_module, hook_name):
                raise AttributeError(
                    f'Backend "{backend_name}" does not have "{hook_name}" function'
                )

            hooks[hook_name].append(getattr(backend_module, hook_name))
            logger.debug(f'Added "{hook_name}" from "{backend_name}" to hooks')

    return hooks
