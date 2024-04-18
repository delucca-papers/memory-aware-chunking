import os
import resource

from resource import struct_rusage
from .base import MemoryUsageBackend
from ..enums import MemoryUsageBackendName
from ....config import ConfigManager
from ....logging import Logger


class ResourceBackend(MemoryUsageBackend):
    unit: str = "kb"
    name: MemoryUsageBackendName = MemoryUsageBackendName.RESOURCE
    _logger: Logger = Logger("ResourceBackend")
    _config: ConfigManager = ConfigManager()

    def get_current_memory_usage(self) -> float:
        return self.__get_memory_usage().ru_maxrss

    def __get_memory_usage(self) -> struct_rusage:
        return resource.getrusage(resource.RUSAGE_SELF)
