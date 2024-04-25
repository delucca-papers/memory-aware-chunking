import inspect

from logging import getLogger, Logger
from toolz import compose
from dowser.common import get_function_path
from .builders import build_logger


def get_logger(logger_name: str | None = None) -> Logger:
    logger_name = logger_name or get_function_path()

    return compose(build_logger, getLogger)(logger_name)


__all__ = ["get_logger"]
