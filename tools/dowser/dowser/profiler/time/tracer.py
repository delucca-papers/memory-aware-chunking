from typing import Any, Tuple
from types import FrameType
from dowser.config import ProfilerMetric


__all__ = ["on_call"]


def on_call(frame: FrameType, event: str, args: Any) -> Tuple[str]:
    return (ProfilerMetric.TIME.value,)
