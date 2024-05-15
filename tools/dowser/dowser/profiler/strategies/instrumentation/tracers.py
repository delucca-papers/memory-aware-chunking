import sys

from typing import Any, Callable, Optional, List
from types import FrameType
from dowser.common.logger import logger
from dowser.profiler.types import TraceHooks, TraceFunction
from .traces import traces


__all__ = ["start_tracer", "stop_tracer"]


def start_tracer(
    socket_path: str,
    depth: int,
    **hooks: TraceHooks,
) -> None:
    logger.info("Starting profile tracer")

    traces.attach_socket(socket_path)
    tracer = build_tracer(depth, hooks)

    execute_hooks(hooks.get("before", []), "before")
    sys.setprofile(tracer)


def stop_tracer(**hooks: TraceHooks) -> None:
    traces.flush()
    sys.setprofile(None)
    logger.info("Profile tracer stopped")
    execute_hooks(hooks.get("after", []), "after")


def build_tracer(max_depth: int, hooks: TraceHooks) -> TraceFunction:
    def tracer(frame: FrameType, event: str, arg: Any) -> Optional[TraceFunction]:
        traces.new_event(event)
        if traces.current_depth >= max_depth:
            return None

        event_key = f"on_{event}"
        if event_key in hooks:
            function = frame.f_code.co_name
            module_name = frame.f_globals.get("__name__", frame.f_code.co_filename)
            source = f"{module_name}:{frame.f_code.co_firstlineno}"

            event_hooks = hooks.get(event_key)
            captured_traces = execute_hooks(event_hooks, event_key, frame, event, arg)

            traces.add_trace(source, function, event, captured_traces)

        return tracer

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
