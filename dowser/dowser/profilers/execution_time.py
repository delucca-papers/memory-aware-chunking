from typing import Callable
from toolz import curry, identity
from ..core.config import config


@curry
def profile(
    config: dict = config,
    function: Callable = identity,
    *function_args,
    **function_kwargs
) -> Callable:
    return function(*function_args, **function_kwargs)


__all__ = ["profile"]
