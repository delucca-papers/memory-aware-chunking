from functools import wraps
from typing import TypedDict, Callable, Any
from memory_profiler import memory_usage
from .base import MemoryUsageBackend
from ..enums import MemoryUsageBackendName
from ....config import ConfigManager
from ....logging import Logger


class MprofBackend(MemoryUsageBackend):
    unit: str = "mb"
    name: MemoryUsageBackendName = MemoryUsageBackendName.MPROF
    _logger: Logger = Logger("MprofBackend")
    _config: ConfigManager = ConfigManager()

    def get_current_memory_usage(self) -> int:
        raise NotImplementedError("With Mprof you shouldn't query current memory usage")

    def start_profiling(self, func: Callable) -> Callable:
        self._logger.debug("Starting memory usage profiler")

        self._update_profiled_function(func)

        @wraps(func)
        def profiled_function(*args, **kwargs) -> Any:
            self._memory_log, result = memory_usage(
                (func, args, kwargs),
                interval=self._precision,
                retval=True,
                timestamps=True,
            )

            return result

        return profiled_function
