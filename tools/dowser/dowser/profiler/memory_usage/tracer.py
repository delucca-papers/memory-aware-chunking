from dowser.profiler.types import TraceFunction
from types import FrameType


__all__ = ["on_call"]


def on_call(frame: FrameType, event: str, args: any) -> TraceFunction:
    return on_call
