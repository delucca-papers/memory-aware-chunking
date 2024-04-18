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
    __pid: str

    def __init__(self, pid: int = os.getpid()):
        super().__init__()
        self.__pid = str(pid)

    def get_current_memory_usage(self) -> float:
        raise NotImplementedError(
            "With KernelBackend, you should seek the file instead"
        )

    def get_peak_memory_usage(self) -> float:
        raise NotImplementedError(
            "With KernelBackend, you should seek the file instead"
        )

    def _monitor_memory_usage(self, output: str) -> None:
        with open(f"/proc/{self.__pid}/status", "r") as status_file:
            while not self._finished_execution.is_set():
                unit = self._config.get_config("dowser.metrics.memory_usage.unit")
                precision = self._get_precision()
                tabs = self._get_tabs_for_unit()
                memory_usage = self.__seek_memory_usage(status_file)
                current_memory_usage, peak_memory_usage = [
                    self._normalize_unit(value) for value in memory_usage
                ]
                timestamp = time.time()

                with open(output, "a") as file:
                    file.write(f"TIME {timestamp}{tabs}")
                    file.write(f"CURRENT {current_memory_usage} {unit}{tabs}")
                    file.write(f"PEAK {peak_memory_usage} {unit}\n")

                time.sleep(precision)

    def __seek_memory_usage(self, status_file: TextIOWrapper) -> tuple[float, float]:
        status_file.seek(0)

        vm_size = None
        vm_peak = None
        for line in status_file:
            if "VmSize" in line:
                vm_size = line.split(":")[1].split()[0].strip()
            elif "VmPeak" in line:
                vm_peak = line.split(":")[1].split()[0].strip()
            if vm_size and vm_peak:
                break

        return float(vm_size), float(vm_peak)
