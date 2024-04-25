import inspect

from logging import getLogger, Logger
from toolz import compose
from .builders import build_logger


def __get_function_path() -> str:
    stack = inspect.stack()
    caller_frame = stack[2]
    module = inspect.getmodule(caller_frame[0])
    module_name = module.__name__
    function_name = caller_frame[3]

    return f"{module_name}.{function_name}"


def get_logger(logger_name: str | None = None) -> Logger:
    logger_name = logger_name or __get_function_path()

    return compose(build_logger, getLogger)(logger_name)


__all__ = ["get_logger"]
