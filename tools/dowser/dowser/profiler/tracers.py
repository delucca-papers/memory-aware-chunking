import sys
import time

from typing import Any, Callable, Tuple, Optional
from types import FrameType
from dowser.common.logger import logger
from .types import TraceHooks, TraceFunction, TraceList


__all__ = ["build_start_tracer", "build_stop_tracer"]


def build_start_tracer(
    depth: int = 3,
    **hooks: TraceHooks,
) -> Tuple[Callable, TraceList]:
    logger.info("Building profile tracer")
    logger.debug(f"Using depth of {depth}")

    traces = []
    tracer = build_tracer(depth, hooks, traces)

    def start_tracer() -> None:
        logger.info("Starting profile tracer")

        before_hooks = hooks.get("before", [])
        for hook in before_hooks:
            hook()

        sys.setprofile(tracer)

    return start_tracer, traces


def build_stop_tracer(**hooks: TraceHooks) -> Callable:
    logger.info("Building stop profile tracer")

    def stop_tracer() -> None:
        sys.setprofile(None)

        logger.info("Stopping profile tracer")

        logger.info("Running after hooks")
        after_hooks = hooks.get("after", [])
        for hook in after_hooks:
            hook()

    return stop_tracer


def build_tracer(depth: int, hooks: TraceHooks, traces: TraceList) -> TraceFunction:
    def tracer(frame: FrameType, event: str, arg: Any) -> Optional[TraceFunction]:
        timestamp = time.time()
        module_name = frame.f_globals.get("__name__", frame.f_code.co_filename)
        source = f"{module_name}:{frame.f_code.co_firstlineno}"
        function_name = frame.f_code.co_name
        event_key = f"on_{event}"

        # We should not store the stop_tracer event, since that would
        # be an orphan trace
        if function_name == "stop_tracer" and "dowser" in source:
            return

        if event_key in hooks.keys():
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

        return build_tracer(depth - 1, hooks, traces) if depth > 0 else None

    return tracer
