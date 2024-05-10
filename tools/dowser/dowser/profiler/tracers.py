import sys
import time
from typing import Any, Callable, Tuple, Optional, List
from types import FrameType
from dowser.common.logger import logger
from .types import (
    TraceHooks,
    TraceFunction,
    TraceList,
    Trace,
    Source,
    Function,
    Event,
    CapturedTrace,
)


__all__ = ["build_start_tracer", "build_stop_tracer"]


def build_start_tracer(
    depth: int = 3,
    **hooks: TraceHooks,
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
    ignored_functions = ["start_tracer", "stop_tracer"]

    def tracer(frame: FrameType, event: str, arg: Any) -> Optional[TraceFunction]:
        nonlocal current_depth
        if event == "call":
            if current_depth >= max_depth:
                return None
            current_depth += 1
        elif event == "return":
            if current_depth > 0:
                current_depth -= 1

        module_name = frame.f_globals.get("__name__", frame.f_code.co_filename)
        source = f"{module_name}:{frame.f_code.co_firstlineno}"
        function = frame.f_code.co_name
        event_key = f"on_{event}"

        if function in ignored_functions:
            return None

        if event_key in hooks:
            event_hooks = hooks.get(event_key)
            captured_traces = execute_hooks(event_hooks, event_key, frame, event, arg)
            trace = build_trace(source, function, event, captured_traces)

            traces.append(trace)

        return tracer if current_depth < max_depth else None

    return tracer


def execute_hooks(hooks: List[Callable], hook_type: str, *args, **kwargs) -> List[Any]:
    hook_results = []

    for hook in hooks:
        try:
            result = hook(*args, **kwargs)
            hook_results.append(result)
        except Exception as e:
            logger.error(f'Error executing "{hook_type}" hook: {e}')

    return hook_results


def build_trace(
    source: Source,
    function: Function,
    event: Event,
    captured_traces: List[CapturedTrace],
) -> Trace:
    return {
        "source": source,
        "function": function,
        "event": event,
        **{key: value for key, value in captured_traces},
    }
