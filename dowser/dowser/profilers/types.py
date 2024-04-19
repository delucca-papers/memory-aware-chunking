from typing import Callable

MemoryUsageLog = tuple[float, str]
MemoryUsageWrappedResult = tuple[MemoryUsageLog, ...]
MemoryUsageWrapper = Callable[..., MemoryUsageWrappedResult]

__all__ = ["MemoryUsageWrapper"]
