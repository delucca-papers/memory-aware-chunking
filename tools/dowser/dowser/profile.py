from typing import Callable
from toolz import compose, identity
from .core import get_logger
from .contexts import config
from .profilers import time, memory_usage

get_enabled_profilers = config.lazy_get("profiler.enabled_profilers")


###


def profile(function: Callable):
    logger = get_logger()
    logger.info(f'Setting up profilers for function "{function.__name__}"')

    enabled_profilers = get_enabled_profilers().split(",")

    with_profilers = compose(
        (memory_usage.profile if "memory_usage" in enabled_profilers else identity),
        (time.profile if "time" in enabled_profilers else identity),
    )

    return with_profilers(function)


__all__ = ["profile"]
