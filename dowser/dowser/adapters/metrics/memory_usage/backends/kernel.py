import os

from .base import MemoryUsageBackend
from ..enums import MemoryUsageBackendName
from ....config import ConfigManager
from ....logging import Logger


class KernelBackend(MemoryUsageBackend):
    unit: str = "kb"
    name: MemoryUsageBackendName = MemoryUsageBackendName.KERNEL
    _logger: Logger = Logger("KernelBackend")
    _config: ConfigManager = ConfigManager()
    __pid: str

    def __init__(self, pid: int = os.getpid()):
        self.__pid = str(pid)
        super().__init__()

    def get_current_memory_usage(self) -> int:
        return self.__get_memory_value("VmSize")

    def get_peak_memory_usage(self) -> int:
        return self.__get_memory_value("VmPeak")

    def __get_memory_value(self, key: str) -> int:
        status = self.__get_status()
        for line in status:
            if key in line:
                return int(line.split()[1])

    def __get_status(self) -> list[str]:
        status_file = open(f"/proc/{self.__pid}/status", "r")
        return status_file.readlines()
