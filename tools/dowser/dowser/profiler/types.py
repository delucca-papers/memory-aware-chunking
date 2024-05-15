from typing import Callable, TypedDict, List, Any, Tuple, Optional, Literal
from types import FrameType


__all__ = [
    "TraceFunction",
    "TraceHooks",
    "TraceList",
    "Trace",
    "CapturedTrace",
    "Source",
    "Function",
    "Event",
    "ExecutorHooks",
]


TraceKey = str
CapturedTrace = Tuple[TraceKey, Any]

Source = str
Function = str
Event = Literal["call", "return"]

TraceFunction = Callable[[FrameType, Event, Any], CapturedTrace]


class Trace(TypedDict):
    source: Source
    function: Function
    event: Event
    kernel_memory_usage: Optional[float]
    psutil_memory_usage: Optional[float]
    resource_memory_usage: Optional[float]
    tracemalloc_memory_usage: Optional[float]
    unix_timestamp: Optional[int]


TraceList = List[Trace]


class TraceHooks(TypedDict):
    on_call: List[TraceFunction]
    on_return: List[TraceFunction]


class ExecutorHooks(TypedDict):
    before: Callable
    after: Callable
