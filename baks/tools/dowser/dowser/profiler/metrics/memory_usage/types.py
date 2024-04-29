from typing import Literal, TypedDict

Timestamp = float
MemoryUsage = float
MemoryUnit = Literal["b", "kb", "mb", "gb"]
MemoryUsageRecord = tuple[Timestamp, MemoryUsage]
MemoryUsageLog = list[MemoryUsageRecord]


class MemoryUsageEntry(TypedDict):
    timestamp: Timestamp
    memory_usage: MemoryUsage


class Metadata(TypedDict):
    backend: str
    precision: float
    function_path: str
    unit: MemoryUnit


MemoryUsageProfile = list[MemoryUsageEntry]


__all__ = [
    "MemoryUsageLog",
    "MemoryUsageRecord",
    "MemoryUsageEntry",
    "MemoryUsageProfile",
    "MemoryUnit",
    "Metadata",
]
