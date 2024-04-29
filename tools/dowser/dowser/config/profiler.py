import uuid

from pydantic import BaseModel, FilePath, field_validator
from enum import Enum


__all__ = ["ProfilerConfig"]


class Metric(Enum):
    MEMORY_USAGE = "MEMORY_USAGE"
    TIME = "TIME"


class MemoryUsageBackend(Enum):
    PSUTIL = "PSUTIL"
    RESOURCE = "RESOURCE"
    TRACEMALLOC = "TRACEMALLOC"
    MPROF = "MPROF"
    KERNEL = "KERNEL"


class MemoryUsageUnit(Enum):
    KB = "KB"
    MB = "MB"
    GB = "GB"


class MemoryUsageConfig(BaseModel):
    enabled_backends: list[MemoryUsageBackend] = [MemoryUsageBackend.KERNEL]
    unit: MemoryUsageUnit = MemoryUsageUnit.MB

    @field_validator("enabled_backends", mode="before")
    def uppercase_enabled_backends(cls, v: any) -> list[MemoryUsageBackend]:
        if isinstance(v, list):
            return [MemoryUsageBackend(i.upper()) for i in v]

        return v

    @field_validator("unit", mode="before")
    def uppercase_unit(cls, v: any) -> MemoryUsageUnit:
        if isinstance(v, str):
            v = v.upper()

        return MemoryUsageUnit(v)


class ProfilerConfig(BaseModel):
    session_id: str = str(uuid.uuid4())
    enabled_metrics: list[Metric] = [Metric.MEMORY_USAGE, Metric.TIME]
    script: FilePath
    args: list[str] = []

    @field_validator("enabled_metrics", mode="before")
    def uppercase_enabled_transports(cls, v: any) -> list[Metric]:
        if isinstance(v, list):
            return [Metric(i.upper()) for i in v]

        return v
