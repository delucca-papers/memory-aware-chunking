import os
import time

from io import TextIOWrapper
from .base import MemoryUsageBackend
from ..enums import MemoryUsageBackendName
from ....config import ConfigManager
from ....logging import Logger


class KernelBackend(MemoryUsageBackend):
    unit: str = "kb"
    name: MemoryUsageBackendName = MemoryUsageBackendName.KERNEL
    _logger: Logger = Logger("KernelBackend")
    _config: ConfigManager = ConfigManager()
    __pid: int

    def __init__(self, pid: int = os.getpid()):
        super().__init__()
        self.__pid = pid

    def get_current_memory_usage(self) -> float:
        raise NotImplementedError(
            "With KernelBackend, you should seek the file instead"
        )

    def _monitor_memory_usage(self) -> None:
        with open(f"/proc/{self.__pid}/status", "r") as status_file:
            while not self._finished_execution.is_set():
                current_memory_usage = self.__seek_memory_usage(status_file)
                timestamp = time.time()

                self._memory_log.append((current_memory_usage, timestamp))

                time.sleep(self._precision)

    def __seek_memory_usage(self, status_file: TextIOWrapper) -> float:
        status_file.seek(0)

        for line in status_file:
            if "VmSize" in line:
                return float(line.split(":")[1].split()[0].strip())
