from typing import Callable
from .config import ConfigManager
from .metrics import (
    Profiler,
    MemoryUsageProfiler,
    MemoryUsageBackendName,
    ProfilerFactory,
    ExecutionTimeProfiler,
)


def profile(
    func: Callable | None = None,
    memory_usage_backend: MemoryUsageBackendName | str | None = None,
    input_metadata: str | None = None,
    enabled_profilers: str = None,
    config: ConfigManager = ConfigManager(),
) -> Callable:
    enabled_profilers = enabled_profilers or config.get_config(
        "dowser.profiler.enabled_profilers"
    )

    profilers = __build_enabled_profilers(
        enabled_profilers,
        memory_usage_backend,
        input_metadata,
    )
    profile = ProfilerFactory.from_profilers(*profilers)

    return profile(func) if func else profile


def __build_enabled_profilers(
    enabled_profilers: str,
    memory_usage_backend: MemoryUsageBackendName | str | None,
    input_metadata: str | None,
) -> list[Profiler]:
    enabled_profilers = enabled_profilers.split(",")

    profilers = []

    if "memory_usage" in enabled_profilers:
        profilers.append(
            __build_memory_usage_profiler(memory_usage_backend, input_metadata)
        )
    if "execution_time" in enabled_profilers:
        profilers.append(ExecutionTimeProfiler())

    return profilers


def __build_memory_usage_profiler(
    memory_usage_backend: MemoryUsageBackendName | str | None = None,
    input_metadata: str | None = None,
) -> MemoryUsageProfiler:
    metrics_config = {"input_metadata": input_metadata}
    return MemoryUsageProfiler.from_backend_name(
        memory_usage_backend
    ).update_backend_config(metrics_config)
