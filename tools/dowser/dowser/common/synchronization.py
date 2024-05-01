from typing import Callable
from functools import wraps


__all__ = ["lazy"]


def lazy(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        @wraps(func)
        def delayed():
            return func(*args, **kwargs)

        return delayed

    return wrapper
