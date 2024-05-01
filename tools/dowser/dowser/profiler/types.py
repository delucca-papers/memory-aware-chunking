from typing import Callable, TypedDict, List, Any, Tuple
from types import FrameType


__all__ = ["TraceFunction", "TraceHooks", "TraceList"]


Event = str
TraceFunction = Callable[[FrameType, Event, Any], Tuple]

Timestamp = str
FilePath = str
FunctionLineNumber = int
FunctionName = str
Trace = Tuple[Timestamp, FilePath, FunctionLineNumber, FunctionName, Event, Any]
TracesList = List[Trace]


class TraceHooks(TypedDict):
    on_call: List[TraceFunction]
    on_return: List[TraceFunction]
