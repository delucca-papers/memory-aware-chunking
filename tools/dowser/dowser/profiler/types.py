from typing import Callable, TypedDict
from types import FrameType


__all__ = ["TraceFunction", "TraceHooks"]


TraceFunction = Callable[[FrameType, str, any], Callable]


class TraceHooks(TypedDict):
    on_call: list[TraceFunction]
    on_return: list[TraceFunction]
