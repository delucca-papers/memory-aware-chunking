import logging
import os
import inspect

from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from toolz import compose, curry, identity
from .config import config

get_output_dir = config.lazy_get("output_dir")
get_filename = config.lazy_get("logging.filename")
get_transports = config.lazy_get("logging.transports")
get_log_level = config.lazy_get("logging.level")
get_formatter = compose(logging.Formatter, config.lazy_get("logging.format"))


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
def set_level(logger: logging.Logger) -> logging.Logger:
    level = get_log_level()
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


def set_transports(logger: logging.Logger) -> logging.Logger:
    transports = get_transports()
    formatter = get_formatter()
    output_dir = get_output_dir()
    filename = get_filename()

    print(output_dir)

    return compose(
        (
            set_file_transport(formatter, output_dir, filename)
            if "file" in transports
            else identity
        ),
        set_console_transport(formatter) if "console" in transports else identity,
    )(logger)


###


get_logger = compose(
    set_transports,
    set_level,
    get_named_logger,
)


__all__ = ["get_logger"]
