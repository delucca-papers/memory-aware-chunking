from typing import Callable

ThreadWrappedResult = tuple[list, ...]
ThreadWrapper = Callable[..., ThreadWrappedResult]

__all__ = ["ThreadWrapper", "ThreadWrappedResult"]
