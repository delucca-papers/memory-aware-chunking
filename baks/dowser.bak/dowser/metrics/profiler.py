import os

from abc import ABC, abstractmethod
from typing import Callable, Any
from functools import wraps
from ..config import ConfigManager


class Profiler(ABC):
    _config: ConfigManager
    _profiled_function: Callable | None = None

    def profile(
        self,
        func: Callable,
    ) -> Callable:
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            return self.execute(func, *func_args, **func_kwargs)

        return wrapper

    @abstractmethod
    def execute(
        self,
        func: Callable,
        *func_args,
        **func_kwargs,
    ) -> Any:
        pass

    @abstractmethod
    def start_profiling(self, func: Callable) -> Callable:
        pass

    def stop_profiling(self) -> None:
        self._logger.debug("Stopping memory usage profiler")

        self._finished_execution.set()
        if self.__profiling_thread:
            self.__profiling_thread.join()

        self.__save_memory_log()

    def _add_headers(
        self,
        filepath: str,
        additional_headers: str | None = None,
    ) -> None:
        execution_id = self._config.get_config("dowser.execution_id")
        input_metadata = self._config.get_config("dowser.metrics.input_metadata")

        with open(filepath, "w") as file:
            file.write(f"Execution ID:\t\t{execution_id}\n")
            file.write(f"Input Metadata:\t\t{input_metadata}\n")
            file.write(f"Function:\t\t\t{self._profiled_function.__name__}\n")
            if additional_headers:
                file.write(additional_headers)
            file.write("\n")

    def _get_metrics_dirpath(self) -> str:
        root_output_dir = self._config.get_config("dowser.output_dir")
        execution_id = self._config.get_config("dowser.execution_id")
        metrics_output_dir = self._config.get_config("dowser.metrics.output_dir")

        dirpath = os.path.join(
            root_output_dir,
            execution_id,
            metrics_output_dir,
        )
        os.makedirs(os.path.dirname(dirpath), exist_ok=True)

        return dirpath
