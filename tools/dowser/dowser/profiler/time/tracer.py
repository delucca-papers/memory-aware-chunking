from dowser.common.types import TraceFunction
from types import FrameType


__all__ = ["trace"]


def trace(frame: FrameType, event: str, args: any) -> TraceFunction:
    return trace
