from functools import wraps


__all__ = ["lazy", "passthrough"]


def lazy(func: callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        @wraps(func)
        def delayed():
            return func(*args, **kwargs)

        return delayed

    return wrapper


def passthrough(*args, **kwargs) -> tuple[tuple, dict]:
    return args, kwargs
