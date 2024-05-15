from typing import Callable
from toolz import curry
from dowser.config import ProfilerInstrumentationConfig
from dowser.common.synchronization import lazy, run_subprocess
from dowser.common.networking import start_socket
from dowser.profiler.types import TraceHooks, ExecutorHooks
from .hooks import before, after
from .socket import consume_socket


__all__ = ["build_executor_hooks"]


@curry
def build_executor_hooks(
    instrumentation_config: ProfilerInstrumentationConfig,
    trace_hooks: TraceHooks,
    on_data: Callable,
) -> ExecutorHooks:
    server = start_socket(instrumentation_config.socket_path)
    run_subprocess(
        consume_socket,
        server,
        instrumentation_config.socket_path,
        on_data,
    )

    return {
        "before": lazy(before)(
            trace_hooks,
            instrumentation_config.socket_path,
            depth=instrumentation_config.depth,
        ),
        "after": lazy(after)(),
    }
