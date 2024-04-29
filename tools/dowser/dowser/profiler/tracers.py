import sys

from types import FrameType
from dowser.common.logger import logger
from .types import TraceHooks, TraceFunction


__all__ = ["start_tracer", "stop_tracer"]


def start_tracer(**hooks: TraceHooks) -> None:
    logger.info("Starting profile tracer")
    enabled_hooks = hooks.keys()

    def trace(frame: FrameType, event: str, arg: any) -> TraceFunction:
        event_key = f"on_{event}"
        if event_key in enabled_hooks:
            for hook in hooks[event_key]:
                hook(frame, event, arg)

        return trace

    sys.settrace(trace)


def stop_tracer() -> None:
    logger.info("Stopping profile tracer")
    sys.settrace(None)
