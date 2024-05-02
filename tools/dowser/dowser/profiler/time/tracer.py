from typing import Any, Tuple
from types import FrameType
from dowser.config import ProfilerMetric


__all__ = ["on_call", "on_return"]


def on_call(_: FrameType, __: str, ___: Any) -> Tuple[str]:
    return (ProfilerMetric.TIME.value,)


on_return = on_call
