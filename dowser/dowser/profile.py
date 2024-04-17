from typing import Callable
from functools import wraps
from .adapters.metrics import MemoryUsageAdapter, MemoryUsageBackendName


def profile(
    func: Callable | None = None,
    memory_usage_backend: MemoryUsageBackendName | None = None,
    input_metadata: str | None = None,
) -> Callable:
    metrics_config = {"input_metadata": input_metadata}
    memory_usage = MemoryUsageAdapter.from_backend_name(
        memory_usage_backend
    ).update_backend_config(metrics_config)

    def decorator(inner_func: Callable) -> Callable:
        @wraps(inner_func)
        def wrapper(*func_args, **func_kwargs):
            return memory_usage.profile(
                inner_func,
                *func_args,
                **func_kwargs,
            )

        return wrapper

    return decorator(func) if func else decorator
