import logging
import os
import inspect

from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from toolz import compose, curry, identity
from .config import get_namespace, get_config

logging_config = get_namespace("logging")
output_dir = get_config("output_dir")
formatter = logging.Formatter(logging_config.get("format"))
log_level = logging_config.get("level")
transports = logging_config.get("transports").split(",")


###


def get_named_logger(name: str | None = None) -> logging.Logger:
    name = name or get_function_path()

    return logging.getLogger(name)


def get_function_path() -> str:
    stack = inspect.stack()
    caller_frame = stack[3]
    module = inspect.getmodule(caller_frame[0])
    module_name = module.__name__
    filtered_module_name = ".".join(module_name.split(".")[1:])
    function_name = caller_frame[3]

    return f"{filtered_module_name}.{function_name}"


@curry
def set_level(level: str, logger: logging.Logger) -> logging.Logger:
    logger.setLevel(level.upper())
    return logger


@curry
def set_console_transport(
    formatter: logging.Formatter,
    logger: logging.Logger,
) -> logging.Logger:
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


@curry
def set_file_transport(
    formatter: logging.Formatter,
    output_dir: str,
    filename: str,
    logger: logging.Logger,
) -> logging.Logger:
    log_filepath = os.path.join(output_dir, filename)
    file_handler = RotatingFileHandler(
        log_filepath,
        maxBytes=10485760,
        backupCount=3,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


###


get_logger = compose(
    (
        set_file_transport(formatter, output_dir, logging_config.get("filename"))
        if "file" in transports
        else identity
    ),
    set_console_transport(formatter) if "console" in transports else identity,
    set_level(log_level),
    get_named_logger,
)


__all__ = ["get_logger"]
