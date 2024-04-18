from functools import wraps
from typing import TypedDict, Callable, Any
from memory_profiler import memory_usage
from .base import MemoryUsageBackend
from ..enums import MemoryUsageBackendName
from ....config import ConfigManager
from ....logging import Logger


class _MprofUsedMemory(TypedDict):
    value: float
    unit: str


class MprofBackend(MemoryUsageBackend):
    unit: str = "mb"
    name: MemoryUsageBackendName = MemoryUsageBackendName.MPROF
    _logger: Logger = Logger("MprofBackend")
    _config: ConfigManager = ConfigManager()
    __memory_history: list[float] = []
    __output_filepath: str = ""

    def start_profiling(self, func: Callable) -> Callable:
        self._logger.debug("Starting memory usage profiler")

        precision = self._get_precision()
        self.__output_filepath = self._build_output_file(func.__name__)

        @wraps(func)
        def profiled_function(*args, **kwargs) -> Any:
            self.__memory_history, result = memory_usage(
                (func, args, kwargs),
                interval=precision,
                retval=True,
                timestamps=True,
            )

            return result

        return profiled_function

    def stop_profiling(self) -> None:
        self._logger.debug("Stopping memory usage profiler")

        unit = self._config.get_config("dowser.metrics.memory_usage.unit")
        tabs = self._get_tabs_for_unit()
        peak_memory_usage = None

        for current_memory_usage, timestamp in self.__memory_history:
            current_memory_usage = self._normalize_unit(current_memory_usage)
            if not peak_memory_usage or current_memory_usage > peak_memory_usage:
                peak_memory_usage = current_memory_usage

            with open(self.__output_filepath, "a") as file:
                file.write(f"TIME {timestamp}{tabs}")
                file.write(f"CURRENT {current_memory_usage} {unit}{tabs}")
                file.write(f"PEAK {peak_memory_usage} {unit}\n")

    def get_current_memory_usage(self) -> int:
        raise NotImplementedError("With Mprof you shouldn't query current memory usage")

    def get_peak_memory_usage(self) -> int:
        raise NotImplementedError("With Mprof you shouldn't query peak memory usage")
