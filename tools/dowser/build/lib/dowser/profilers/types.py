from typing import Callable

MemoryUsage = tuple[float, str]
MemoryUsageLog = list[MemoryUsage]
MemoryUsageWrappedResult = tuple[MemoryUsageLog, ...]
MemoryUsageWrapper = Callable[..., MemoryUsageWrappedResult]

Time = tuple[str, float]
TimeLog = list[Time]

__all__ = ["MemoryUsageWrapper", "MemoryUsageLog", "MemoryUsage", "TimeLog", "Time"]
