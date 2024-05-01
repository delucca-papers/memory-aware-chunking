import sys
import time

from typing import Any, Callable, Tuple
from types import FrameType
from dowser.common.logger import logger
from .types import TraceHooks, TraceFunction, TracesList


__all__ = ["build_tracer", "stop_tracer"]


def build_tracer(**hooks: TraceHooks) -> Tuple[Callable, TracesList]:
    logger.info("Building profile tracer")
    enabled_hooks = hooks.keys()
    traces = []

    def start_tracer() -> None:
        logger.info("Starting profile tracer")

        def collect_trace(frame: FrameType, event: str, arg: Any) -> TraceFunction:
            timestamp = time.time()
            file_path = frame.f_code.co_filename
            function_line_number = frame.f_code.co_firstlineno
            function_name = frame.f_code.co_name
            event_key = f"on_{event}"

            if event_key in enabled_hooks:
                for hook in hooks[event_key]:
                    trace = hook(frame, event, arg)
                    traces.append(
                        (
                            timestamp,
                            file_path,
                            function_line_number,
                            function_name,
                            event,
                            *trace,
                        )
                    )

            return collect_trace

        sys.settrace(collect_trace)

    return start_tracer, traces


def stop_tracer() -> None:
    logger.info("Stopping profile tracer")
    sys.settrace(None)
