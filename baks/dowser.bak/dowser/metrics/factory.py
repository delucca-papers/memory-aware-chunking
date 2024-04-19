from typing import Callable
from .profiler import Profiler
from ..config import ConfigManager


class ProfilerFactory:
    @staticmethod
    def from_profilers(*profilers: Profiler) -> Callable:
        def decorator(func: Callable) -> Callable:
            profiled_func = func
            for profiler in profilers:
                profiled_func = profiler.profile(profiled_func)

            return profiled_func

        return decorator
