from typing import Literal

Timestamp = float
MemoryUsage = float
MemoryUnit = Literal["b", "kb", "mb", "gb"]

MemoryUsageRecord = tuple[Timestamp, MemoryUsage, MemoryUnit]
MemoryUsageLog = list[MemoryUsageRecord]


__all__ = ["MemoryUsageLog", "MemoryUsageRecord"]
