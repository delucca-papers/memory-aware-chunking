import sys
import time

from types import FrameType
from typing import Any, Callable
from toolz import curry
from .types import TimeLog


def trace_call(time_log: TimeLog, frame: FrameType) -> None:
    trace_event(time_log, frame, "CALL")


def trace_return(time_log: TimeLog, frame: FrameType) -> None:
    trace_event(time_log, frame, "RETURN")


def function_path_from_frame(frame: FrameType) -> str:
    module_name = frame.f_globals.get("__name__")
    function_name = frame.f_code.co_name

    return f"{module_name}.{function_name}"


available_tracers = {
    "call": trace_call,
    "return": trace_return,
}


@curry
def trace(time_log: TimeLog, frame: FrameType, event: str, _: Any) -> Callable | None:
    tracer = available_tracers.get(event)

    if tracer is not None:
        tracer(time_log, frame)
        return trace(time_log)

    return


def trace_event(time_log: TimeLog, frame: FrameType, event: str) -> None:
    timestamp = time.time()
    function_path = function_path_from_frame(frame)

    time_log.append((timestamp, event, function_path))


def start_tracer(time_log: TimeLog | None = None) -> TimeLog:
    time_log = time_log or []

    tracer = trace(time_log)
    sys.settrace(tracer)

    return time_log


def stop_tracer() -> None:
    sys.settrace(None)


__all__ = ["start_tracer", "stop_tracer"]
