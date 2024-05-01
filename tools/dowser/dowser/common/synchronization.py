from typing import Callable
from functools import wraps


__all__ = ["lazy", "passthrough"]


def lazy(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        @wraps(func)
        def delayed():
            return func(*args, **kwargs)

        return delayed

    return wrapper


def passthrough(*args, **kwargs):
    return args, kwargs
