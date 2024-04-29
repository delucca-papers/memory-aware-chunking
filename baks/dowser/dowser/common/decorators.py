from typing import Callable
from functools import wraps


def lazy(function: Callable) -> Callable:
    @wraps(function)
    def wrapper(*args, **kwargs) -> Callable:
        return lambda: function(*args, **kwargs)

    return wrapper


__all__ = ["lazy"]
