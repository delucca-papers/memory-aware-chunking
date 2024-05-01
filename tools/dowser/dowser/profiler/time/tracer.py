from typing import Any
from types import FrameType
from dowser.profiler.types import TraceFunction


__all__ = ["on_call"]


def on_call(frame: FrameType, event: str, args: Any) -> TraceFunction:
    return on_call
