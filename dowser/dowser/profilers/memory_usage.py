import importlib

from typing import Callable, Any
from toolz import compose
from functools import wraps
from ..core.config import config, get_namespace, get_config
from ..core.logging import get_logger

get_profiler_config = lambda c: get_namespace("profiler", c)
get_memory_usage_profiler_config = lambda c: get_namespace("memory_usage", c)

get_backend_name = lambda c: compose(
    lambda c: get_config("backend", c),
    get_memory_usage_profiler_config,
    get_profiler_config,
)(c)
get_precision = lambda c: compose(
    lambda p: 10**-p,
    lambda c: float(get_config("precision", c)),
    get_memory_usage_profiler_config,
    get_profiler_config,
)(c)

###


def with_backend(function: Callable, config: dict = config) -> Any:
    logger = get_logger()
    backend_name = get_backend_name(config)
    precision = get_precision(config)
    logger.debug(f'Executing message usage profiler with "{backend_name}" backend')

    backend_module = importlib.import_module(
        f".backends.{backend_name}",
        package=__package__,
    )
    if backend_module is None:
        logger.error(f'Backend "{backend_name}" is not implemented yet')
        return

    backend_wrapper = getattr(backend_module, "wrapper")

    return backend_wrapper(function, precision)


###


def profile(config: dict = config) -> Callable:
    logger = get_logger()
    def decorator(function: Callable) -> Callable:
        logger.info(
            f'Setting up memory usage profiler for function "{function.__name__}"'
        )

        profiled_function = with_backend(function, config=config)

        @wraps(profiled_function)
        def wrapper(*args, **kwargs) -> Any:
            profiler_results, function_results = profiled_function(*args, **kwargs)

            logger.debug(f"Profiler results: {profiler_results}")

            return function_results

        return wrapper

    return decorator


__all__ = ["profile"]
