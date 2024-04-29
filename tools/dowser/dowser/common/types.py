from typing import Callable
from types import FrameType


__all__ = ["TraceFunction"]


TraceFunction = Callable[[FrameType, str, any], Callable]
