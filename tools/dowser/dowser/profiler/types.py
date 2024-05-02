from typing import Callable, TypedDict, List, Any, Tuple
from types import FrameType
from dowser.config import ProfilerMetric


__all__ = ["TraceFunction", "TraceHooks", "TraceList"]


Event = str
TraceFunction = Callable[[FrameType, Event, Any], Tuple]

Timestamp = str
Source = str
FunctionName = str
Trace = Tuple[
    Timestamp,
    Source,
    FunctionName,
    Event,
    ProfilerMetric,
    Any,
]
TraceList = List[Trace]


class TraceHooks(TypedDict):
    on_call: List[TraceFunction]
    on_return: List[TraceFunction]
