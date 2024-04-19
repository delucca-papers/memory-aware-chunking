import time
import os

from abc import ABC, abstractmethod
from threading import Event, Thread
from datetime import datetime
from typing import Any, Callable
from ..enums import MemoryUsageBackendName
from ..types import MemoryUsage
from ....logging import Logger
from ....config import ConfigManager


class MemoryUsageBackend(ABC):
    unit: str
    name: MemoryUsageBackendName
    _logger: Logger
    _config: ConfigManager
    _start_timestamp: str
    _precision: float
    _memory_log: list[MemoryUsage] = []
    _profiled_function: Callable | None = None
    _finished_execution: Event
    __profiling_thread: Thread | None = None

    @abstractmethod
    def get_current_memory_usage(self) -> float:
        pass

    def __init__(self):
        self._start_timestamp = self.__get_formatted_timestamp()
        self._precision = self.__get_precision()
        self._finished_execution = Event()

    def start_profiling(self, func: Callable) -> Callable:
        self._logger.debug("Starting memory usage profiler")

        self._update_profiled_function(func)
        self.__profiling_thread = Thread(target=self._monitor_memory_usage)
        self.__profiling_thread.start()

        return func

    def stop_profiling(self) -> None:
        self._logger.debug("Stopping memory usage profiler")

        self._finished_execution.set()
        if self.__profiling_thread:
            self.__profiling_thread.join()

        self.__save_memory_log()

    def update_config(self, config: dict[str, Any]) -> None:
        self._config.update_config(config, "dowser.metrics")

    def _monitor_memory_usage(self) -> None:
        while not self._finished_execution.is_set():
            current_memory_usage = self.get_current_memory_usage()
            timestamp = time.time()

            self._memory_log.append((current_memory_usage, timestamp))

            time.sleep(self._precision)

    def _update_profiled_function(self, func: Callable) -> None:
        self._profiled_function = func

    def __save_memory_log(self) -> str:
        filepath = self.__get_filepath()

        self.__add_headers(filepath)
        self.__add_memory_log(filepath)

        return filepath

    def __add_headers(self, filepath: str) -> None:
        execution_id = self._config.get_config("dowser.execution_id")
        input_metadata = self._config.get_config("dowser.metrics.input_metadata")

        with open(filepath, "w") as file:
            file.write(f"Execution ID:\t\t{execution_id}\n")
            file.write(f"Backend:\t\t\t{self.name.value}\n")
            file.write(f"Precision:\t\t\t{str(self._precision)}s\n")
            file.write(f"Input Metadata:\t\t{input_metadata}\n")
            file.write(f"Function:\t\t\t{self._profiled_function.__name__}\n")
            file.write("\n")

    def __add_memory_log(self, filepath: str) -> None:
        unit = self._config.get_config("dowser.metrics.memory_usage.unit")
        tabs = self.__get_tabs_for_unit()
        current_peak_memory_usage = None

        with open(filepath, "a") as file:
            for current_memory_usage, timestamp in self._memory_log:
                current_memory_usage = self.__normalize_unit(current_memory_usage)
                if (
                    not current_peak_memory_usage
                    or current_memory_usage > current_peak_memory_usage
                ):
                    current_peak_memory_usage = current_memory_usage

                file.write(f"TIME {timestamp}{tabs}")
                file.write(f"CURRENT {current_memory_usage} {unit}{tabs}")
                file.write(f"PEAK {current_peak_memory_usage} {unit}\n")

    def __get_precision(self) -> float:
        precision = self._config.get_config(
            "dowser.metrics.memory_usage.precision", int
        )

        return 10**-precision

    def __normalize_unit(self, value: int) -> float:
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

    def __get_tabs_for_unit(self) -> str:
        tabs_per_unit = {
            "b": "\t\t\t\t",
            "kb": "\t\t\t",
            "mb": "\t\t",
            "gb": "\t",
        }
        unit = self._config.get_config("dowser.metrics.memory_usage.unit")

        return tabs_per_unit[unit]

    def __get_filepath(self) -> str:
        execution_id = self._config.get_config("dowser.execution_id")
        root_output_dir = self._config.get_config("dowser.output_dir")
        metrics_output_dir = self._config.get_config("dowser.metrics.output_dir")
        memory_usage_output_dir = self._config.get_config(
            "dowser.metrics.memory_usage.output_dir"
        )

        filename = self.__build_base_filename()
        filepath = os.path.join(
            execution_id,
            root_output_dir,
            metrics_output_dir,
            memory_usage_output_dir,
            filename,
        )
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        return filepath

    def __build_base_filename(self) -> str:
        prefix = self._config.get_config("dowser.metrics.memory_usage.filename_prefix")
        suffix = self._config.get_config("dowser.metrics.memory_usage.filename_suffix")

        return f"{prefix}{self._start_timestamp}-{self.name.value}{suffix}.dat"

    def __get_formatted_timestamp(self) -> str:
        return datetime.now().strftime("%Y%m%d%H%M%S")
