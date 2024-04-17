import time
import os

from abc import ABC, abstractmethod
from threading import Event, Thread
from datetime import datetime
from typing import Any
from ..enums import MemoryUsageBackendName
from ....logging import Logger
from ....config import ConfigManager


class MemoryUsageBackend(ABC):
    unit: str
    name: MemoryUsageBackendName
    _logger: Logger
    _config: ConfigManager
    _finished_execution: Event
    _profiling_thread: Thread

    @abstractmethod
    def get_current_memory_usage(self) -> int:
        pass

    @abstractmethod
    def get_peak_memory_usage(self) -> int:
        pass

    def start_profiling(self, func_name: str) -> Event:
        self._logger.debug("Starting memory usage profiler")

        precision = self._config.get_config(
            "dowser.metrics.memory_usage.precision", int
        )
        output = self.__build_output_file(func_name)

        self._profiling_thread = Thread(
            target=self.__monitor_memory_usage,
            args=(precision, output),
        )
        self._profiling_thread.start()

    def stop_profiling(self) -> Event:
        self._logger.debug("Stopping memory usage profiler")

        self._finished_execution.set()
        if self._profiling_thread:
            self._profiling_thread.join()

    def update_config(self, config: dict[str, Any]) -> None:
        self._config.update_config(config, "dowser.metrics")

    def _add_headers(self, filepath: str, func_name: str) -> None:
        execution_id = self._config.get_config("dowser.execution_id")
        input_metadata = self._config.get_config("dowser.metrics.input_metadata")

        with open(filepath, "w") as file:
            file.write(f"Execution ID:\t\t{execution_id}\n")
            file.write(f"Backend:\t\t\t{self.name.value}\n")
            file.write(f"Input Metadata:\t\t{input_metadata}\n")
            file.write(f"Function:\t\t\t{func_name}\n")
            file.write("\n")

    def __monitor_memory_usage(self, precision: int, output: str) -> None:
        while not self._finished_execution.is_set():
            current_memory_usage = self.get_current_memory_usage()
            peak_memory_usage = self.get_peak_memory_usage()
            timestamp = time.time()

            with open(output, "a") as file:
                file.write(f"TIME\t{timestamp}\t")
                file.write(f"CURRENT\t{current_memory_usage} {self.unit}\t")
                file.write(f"PEAK\t{peak_memory_usage} {self.unit}\n")

            time.sleep(10**-precision)

    def __build_output_file(self, func_name: str) -> str:
        root_output_dir = self._config.get_config("dowser.output_dir")
        memory_usage_output_dir = self._config.get_config(
            "dowser.metrics.memory_usage.output_dir"
        )
        prefix = self._config.get_config("dowser.metrics.memory_usage.filename_prefix")
        suffix = self._config.get_config("dowser.metrics.memory_usage.filename_suffix")
        timestamp = self.__get_timestamp()

        filename = f"{prefix}{timestamp}{suffix}.dat"
        filepath = os.path.join(root_output_dir, memory_usage_output_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        self._add_headers(filepath, func_name)

        return filepath

    def __get_timestamp(self) -> str:
        return datetime.now().strftime("%Y%m%d%H%M%S")
