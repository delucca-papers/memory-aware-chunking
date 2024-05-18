import sys

from typing import Any, Callable, Optional, List
from types import FrameType
from dowser.common.logger import logger
from dowser.profiler.types import TraceHooks, TraceFunction
from dowser.profiler.buffer import Buffer


__all__ = ["start_tracer", "stop_tracer"]


def start_tracer(depth: int, buffer: Buffer, **hooks: TraceHooks) -> None:
    logger.info("Starting profile tracer")

    tracer = build_tracer(depth, buffer, hooks)

    execute_hooks(hooks.get("before", []), "before")
    sys.setprofile(tracer)


def stop_tracer(buffer: Buffer, **hooks: TraceHooks) -> None:
    sys.setprofile(None)
    buffer.flush()
    logger.info("Profile tracer stopped")
    execute_hooks(hooks.get("after", []), "after")


def build_tracer(max_depth: int, buffer: Buffer, hooks: TraceHooks) -> TraceFunction:
    def tracer(frame: FrameType, event: str, arg: Any) -> Optional[TraceFunction]:
        if max_depth >= 0 and buffer.current_depth >= max_depth:
            buffer.new_event(event)
            return None

        event_key = f"on_{event}"
        if event_key in hooks:
            function = frame.f_code.co_name
            module_name = frame.f_globals.get("__name__", frame.f_code.co_filename)
            source = f"{module_name}:{frame.f_code.co_firstlineno}"
            event_hooks = hooks.get(event_key)

            captured_traces = execute_hooks(event_hooks, event_key, frame, event, arg)
            buffer.append(source, function, event, captured_traces)

        buffer.new_event(event)

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
