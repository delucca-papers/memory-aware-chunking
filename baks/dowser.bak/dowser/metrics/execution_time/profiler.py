import time
import os

from typing import Callable, Any
from ..profiler import Profiler
from ...logging import Logger


class ExecutionTimeProfiler(Profiler):
    __logger: Logger = Logger("ExecutionTimeProfiler")

    def execute(
        self,
        func: Callable,
        *func_args,
        **func_kwargs,
    ) -> Any:
        self.__logger.debug(f"Capturing execution time for function: {func.__name__}")

        start_time = time.time()
        result = func(*func_args, **func_kwargs)
        end_time = time.time()

        return result
