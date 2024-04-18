import os

from psutil import Process
from typing import NamedTuple
from .base import MemoryUsageBackend
from ..enums import MemoryUsageBackendName
from ....config import ConfigManager
from ....logging import Logger


class PsutilBackend(MemoryUsageBackend):
    unit: str = "b"
    name: MemoryUsageBackendName = MemoryUsageBackendName.PSUTIL
    _logger: Logger = Logger("PsutilBackend")
    _config: ConfigManager = ConfigManager()
    __pid: int
    __process: Process

    def __init__(self, pid: int = os.getpid()):
        super().__init__()
        self.__pid = pid
        self.__process = Process(pid=self.__pid)

    def get_current_memory_usage(self) -> float:
        return self.__get_memory_info().rss

    def __get_memory_info(self) -> NamedTuple:
        return self.__process.memory_info()
