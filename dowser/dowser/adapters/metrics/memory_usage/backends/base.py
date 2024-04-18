import time
import os

from abc import ABC, abstractmethod
from threading import Event, Thread
from datetime import datetime
from typing import Any, Callable
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
    def get_current_memory_usage(self) -> float:
        pass

    @abstractmethod
    def get_peak_memory_usage(self) -> float:
        pass

    def __init__(self):
        self._finished_execution = Event()

    def start_profiling(self, func: Callable) -> Callable:
        self._logger.debug("Starting memory usage profiler")

        output = self._build_output_file(func.__name__)

        self._profiling_thread = Thread(
            target=self._monitor_memory_usage,
            args=(output,),
        )
        self._profiling_thread.start()

        return func

    def stop_profiling(self) -> Event:
        self._logger.debug("Stopping memory usage profiler")

        self._finished_execution.set()
        if self._profiling_thread:
            self._profiling_thread.join()

    def update_config(self, config: dict[str, Any]) -> None:
        self._config.update_config(config, "dowser.metrics")

    def _build_output_file(self, func_name: str) -> str:
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

    def _get_precision(self) -> float:
        precision = self._config.get_config(
            "dowser.metrics.memory_usage.precision", int
        )

        return 10**-precision

    def _add_headers(self, filepath: str, func_name: str) -> None:
        execution_id = self._config.get_config("dowser.execution_id")
        input_metadata = self._config.get_config("dowser.metrics.input_metadata")
        precision = self._get_precision()

        with open(filepath, "w") as file:
            file.write(f"Execution ID:\t\t{execution_id}\n")
            file.write(f"Backend:\t\t\t{self.name.value}\n")
            file.write(f"Precision:\t\t\t{str(precision)}s\n")
            file.write(f"Input Metadata:\t\t{input_metadata}\n")
            file.write(f"Function:\t\t\t{func_name}\n")
            file.write("\n")

    def _normalize_unit(self, value: int) -> float:
        conversion = {
            "b_to_kb": 1024,
            "b_to_mb": 1024**2,
            "b_to_gb": 1024**3,
            "kb_to_b": 1 / 1024,
            "kb_to_mb": 1024,
            "kb_to_gb": 1024**2,
            "mb_to_b": 1 / 1024**2,
            "mb_to_kb": 1 / 1024,
            "mb_to_gb": 1024,
            "gb_to_b": 1 / 1024**3,
            "gb_to_kb": 1 / 1024**2,
            "gb_to_mb": 1 / 1024,
        }

        conversion_key = f"{self.unit}_to_{self._config.get_config('dowser.metrics.memory_usage.unit')}"
        if conversion_key in conversion:
            return float(value / conversion[conversion_key])

        return value

    def _get_tabs_for_unit(self) -> str:
        tabs_per_unit = {
            "b": "\t\t\t\t",
            "kb": "\t\t\t",
            "mb": "\t\t",
            "gb": "\t",
        }
        unit = self._config.get_config("dowser.metrics.memory_usage.unit")

        return tabs_per_unit[unit]

    def _monitor_memory_usage(self, output: str) -> None:
        while not self._finished_execution.is_set():
            unit = self._config.get_config("dowser.metrics.memory_usage.unit")
            precision = self._get_precision()
            tabs = self._get_tabs_for_unit()
            current_memory_usage = self._normalize_unit(self.get_current_memory_usage())
            peak_memory_usage = self._normalize_unit(self.get_peak_memory_usage())
            timestamp = time.time()

            with open(output, "a") as file:
                file.write(f"TIME {timestamp}{tabs}")
                file.write(f"CURRENT {current_memory_usage} {unit}{tabs}")
                file.write(f"PEAK {peak_memory_usage} {unit}\n")

            time.sleep(precision)

    def __get_timestamp(self) -> str:
        return datetime.now().strftime("%Y%m%d%H%M%S")
