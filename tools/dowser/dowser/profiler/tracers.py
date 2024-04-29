import sys

from types import FrameType
from dowser.common.logger import logger
from dowser.common.types import TraceFunction


__all__ = ["start_tracer", "stop_tracer"]


def start_tracer(*tracers: list[TraceFunction]) -> None:
    logger.info("Starting profile tracer")

    def trace(frame: FrameType, event: str, arg: any) -> TraceFunction:
        for tracer in tracers:
            tracer(frame, event, arg)
        return trace

    sys.settrace(trace)


def stop_tracer() -> None:
    logger.info("Stopping profile tracer")
    sys.settrace(None)
