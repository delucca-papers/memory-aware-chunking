from typing import Callable, Any
from logging import Logger
from functools import wraps
from toolz import compose
from ..config import config, get_namespace, get_config
from ..logging import get_logger

module_logger = get_logger("profilers.memory_usage")
get_profiler_config = lambda c: get_namespace("profiler", c)
get_memory_usage_profiler_config = lambda c: get_namespace("memory_usage", c)
get_backend_name = lambda c: compose(
    lambda c: get_config("backend", c),
    get_memory_usage_profiler_config,
    get_profiler_config,
)(c)


###


def with_backend(
    config: dict,
    function: Callable,
    logger: Logger = module_logger,
) -> Any:
    backend_name = get_backend_name(config)
    logger.debug(f'Executing message usage profiler with "{backend_name}" backend')

    backend_wrapper = globals().get(f"with_{backend_name}_backend")
    if backend_wrapper is None:
        logger.error(f'Backend "{backend_name}" is not implemented yet')
        return

    return backend_wrapper(config, function)


def with_kernel_backend(
    config: dict,
    function: Callable,
    logger=get_logger("profilers.memory_usage.kernel"),
):
    @wraps(function)
    def wrapped_function(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapped_function


###


def profile(
    config: dict = config,
    logger: Logger = module_logger,
) -> Callable:
    def decorator(function: Callable):
        logger.debug(
            f'Setting up memory usage profiler for function "{function.__name__}"'
        )

        return with_backend(config, function)

    return decorator


__all__ = ["profile"]
