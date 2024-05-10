import sys
import time
from typing import Any, Callable, Tuple, Optional, List
from types import FrameType
from dowser.common.logger import logger
from .types import TraceHooks, TraceFunction, TraceList


__all__ = ["build_start_tracer", "build_stop_tracer"]


def build_start_tracer(
    depth: int = 3, **hooks: TraceHooks
) -> Tuple[Callable, TraceList]:
    logger.info("Building start profile tracer")
    traces = []
    tracer = build_tracer(depth, hooks, traces)

    def start_tracer() -> None:
        logger.info("Starting profile tracer")
        execute_hooks(hooks.get("before", []), "before")
        sys.setprofile(tracer)

    return start_tracer, traces


def build_stop_tracer(**hooks: TraceHooks) -> Callable:
    logger.info("Building stop profile tracer")

    def stop_tracer() -> None:
        sys.setprofile(None)
        logger.info("Profile tracer stopped")
        execute_hooks(hooks.get("after", []), "after")

    return stop_tracer


def build_tracer(max_depth: int, hooks: TraceHooks, traces: TraceList) -> TraceFunction:
    current_depth = 0

    def tracer(frame: FrameType, event: str, arg: Any) -> Optional[TraceFunction]:
        nonlocal current_depth
        if event == "call":
            if current_depth >= max_depth:
                return None
            current_depth += 1
        elif event == "return":
            if current_depth > 0:
                current_depth -= 1

        timestamp = time.time()
        module_name = frame.f_globals.get("__name__", frame.f_code.co_filename)
        source = f"{module_name}:{frame.f_code.co_firstlineno}"
        function_name = frame.f_code.co_name
        event_key = f"on_{event}"

        # Avoid tracing the stop_tracer function, if we
        # allow this we would have orphan traces
        if function_name == "stop_tracer" and "dowser" in source:
            return None

        if event_key in hooks and event != "return":
            event_traces = [hook(frame, event, arg) for hook in hooks[event_key]]
            traces.append((timestamp, source, function_name, event, event_traces))

        return tracer if current_depth < max_depth else None

    return tracer


def execute_hooks(hooks: List[Callable], hook_type: str) -> None:
    for hook in hooks:
        try:
            hook()
        except Exception as e:
            logger.error(f"Error executing {hook_type} hook: {e}")
