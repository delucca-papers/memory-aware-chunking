from typing import Callable, TypedDict, List, Any
from types import FrameType


__all__ = ["TraceFunction", "TraceHooks"]


TraceFunction = Callable[[FrameType, str, Any], Callable]


class TraceHooks(TypedDict):
    on_call: List[TraceFunction]
    on_return: List[TraceFunction]
