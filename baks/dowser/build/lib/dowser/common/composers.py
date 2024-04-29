from typing import Any


def passthrough(*args, **kwargs) -> Any:
    return args, kwargs


__all__ = ["passthrough"]
