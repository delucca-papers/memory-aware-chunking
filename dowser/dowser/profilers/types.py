from typing import Callable

MemoryUsage = tuple[float, str]
MemoryUsageLog = list[MemoryUsage]
MemoryUsageWrappedResult = tuple[MemoryUsageLog, ...]
MemoryUsageWrapper = Callable[..., MemoryUsageWrappedResult]

__all__ = ["MemoryUsageWrapper", "MemoryUsageLog", "MemoryUsage"]
