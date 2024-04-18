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
    __memory_history: list[int] = []

    def get_current_memory_usage(self) -> int:
        memory_usage = self.__get_memory_usage().ru_maxrss
        self.__memory_history.append(memory_usage)

        return memory_usage

    def get_peak_memory_usage(self) -> int:
        return max(self.__memory_history)

    def __get_memory_usage(self) -> struct_rusage:
        return resource.getrusage(resource.RUSAGE_SELF)
