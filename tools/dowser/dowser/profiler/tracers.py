import sys
import time

from typing import Any, Callable, Tuple
from types import FrameType
from dowser.common.logger import logger
from .types import TraceHooks, TraceFunction, TraceList


__all__ = ["build_start_tracer", "build_stop_tracer"]


def build_start_tracer(**hooks: TraceHooks) -> Tuple[Callable, TraceList]:
    logger.info("Building profile tracer")
    enabled_hooks = hooks.keys()
    traces = []

    def start_tracer() -> None:
        logger.info("Starting profile tracer")

        logger.info("Running before hooks")
        before_hooks = hooks.get("before", [])
        for hook in before_hooks:
            hook()

        def collect_trace(frame: FrameType, event: str, arg: Any) -> TraceFunction:
            timestamp = time.time()
            source = f"{frame.f_code.co_filename}:{frame.f_code.co_firstlineno}"
            function_name = frame.f_code.co_name
            event_key = f"on_{event}"

            # We should not store the stop_tracer event, since that would
            # be an orphan trace
            if function_name == "stop_tracer" and "dowser" in source:
                return

            if event_key in enabled_hooks:
                event_traces = [hook(frame, event, arg) for hook in hooks[event_key]]
                traces.append(
                    (
                        timestamp,
                        source,
                        function_name,
                        event,
                        event_traces,
                    )
                )

            return collect_trace

        sys.settrace(collect_trace)

    return start_tracer, traces


def build_stop_tracer(**hooks: TraceHooks) -> Callable:
    logger.info("Building stop profile tracer")

    def stop_tracer() -> None:
        sys.settrace(None)

        logger.info("Stopping profile tracer")

        logger.info("Running after hooks")
        after_hooks = hooks.get("after", [])
        for hook in after_hooks:
            hook()

    return stop_tracer
