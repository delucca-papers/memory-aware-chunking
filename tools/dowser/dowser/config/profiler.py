import uuid
import importlib

from pydantic import BaseModel, FilePath, field_validator
from typing import Optional, List, Any
from enum import Enum


__all__ = ["ProfilerConfig", "Metric", "MemoryUsageBackend"]


class Metric(Enum):
    MEMORY_USAGE = "MEMORY_USAGE"
    TIME = "TIME"


class MemoryUsageBackend(Enum):
    PSUTIL = "PSUTIL"
    RESOURCE = "RESOURCE"
    TRACEMALLOC = "TRACEMALLOC"
    KERNEL = "KERNEL"


class MemoryUsageConfig(BaseModel):
    enabled_backends: List[MemoryUsageBackend] = [MemoryUsageBackend.KERNEL]

    @field_validator("enabled_backends", mode="before")
    def uppercase_enabled_backends(cls, v: Any) -> List[MemoryUsageBackend]:
        if isinstance(v, list):
            return [
                MemoryUsageBackend(i.upper()) if isinstance(i, str) else i for i in v
            ]

        return v


class ProfilerConfig(BaseModel):
    session_id: str = str(uuid.uuid4())
    enabled_metrics: List[Metric] = [Metric.MEMORY_USAGE, Metric.TIME]
    memory_usage: MemoryUsageConfig
    filepath: Optional[FilePath] = None
    entrypoint: Optional[str] = None
    args: tuple = tuple()
    kwargs: dict = {}

    @field_validator("enabled_metrics", mode="before")
    def uppercase_enabled_transports(cls, v: Any) -> List[Metric]:
        if isinstance(v, list):
            return [Metric(i.upper()) if isinstance(i, str) else i for i in v]

        return v

    @field_validator("kwargs", mode="before")
    def parse_kwargs(cls, v: Any):
        if isinstance(v, dict):
            return v
        if isinstance(v, list):
            result = {}
            for item in v:
                if "=" in item:
                    key, value = item.split("=", 1)
                    result[key] = value
                else:
                    raise ValueError(f"Invalid format for kwarg: {item}")
            return result

        raise TypeError("kwarg must be a list of strings or a dict")

    @field_validator("entrypoint")
    def check_function_exists(cls, v: Any, values):
        if v is None:
            return v
        filepath = values.data.get("filepath")
        if filepath is None:
            raise ValueError("File path must be set before checking function")

        spec = importlib.util.spec_from_file_location("module.name", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, v):
            raise ValueError(f"Function '{v}' not found in {filepath}")
        return v
