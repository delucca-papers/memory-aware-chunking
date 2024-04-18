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
    __memory_history: list[int] = []

    def __init__(self, pid: int = os.getpid()):
        super().__init__()
        self.__pid = pid

    def get_current_memory_usage(self) -> int:
        memory_usage = self.__get_memory_info().rss
        self.__memory_history.append(memory_usage)

        return memory_usage

    def get_peak_memory_usage(self) -> int:
        return max(self.__memory_history)

    def __get_memory_info(self) -> NamedTuple:
        process = Process(pid=self.__pid)
        return process.memory_info()
