import tracemalloc
import os

from typing import Callable
from .base import MemoryUsageBackend
from ..enums import MemoryUsageBackendName
from ....config import ConfigManager
from ....logging import Logger


class TraceMallocBackend(MemoryUsageBackend):
    unit: str = "b"
    name: MemoryUsageBackendName = MemoryUsageBackendName.TRACEMALLOC
    _logger: Logger = Logger("TraceMallocBackend")
    _config: ConfigManager = ConfigManager()

    def __init__(self):
        tracemalloc.start()
        super().__init__()

    def get_current_memory_usage(self) -> float:
        current, _ = tracemalloc.get_traced_memory()
        return float(current)

    def stop_profiling(self) -> None:
        tracemalloc.stop()
        super().stop_profiling()
