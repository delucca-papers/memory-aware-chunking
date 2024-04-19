import logging
import os
import inspect

from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from toolz import compose, curry, identity
from .config import get_namespace, get_config, config

get_logging_config = lambda c: get_namespace("logging", c)
get_output_dir = lambda c: get_config("output_dir", c)

get_filename = lambda c: compose(
    lambda c: get_config("filename", c), get_logging_config
)(c)
get_formatter = lambda c: compose(
    logging.Formatter, lambda c: get_config("level", c), get_logging_config
)(c)
get_log_level = lambda c: compose(
    lambda c: get_config("level", c),
    get_logging_config,
)(c)
get_transports = lambda c: compose(
    lambda c: get_config("transports", c),
    get_logging_config,
)(c)


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
def set_level(logger: logging.Logger, config: dict = config) -> logging.Logger:
    level = get_log_level(config)
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


def set_transports(logger: logging.Logger, config: dict = config) -> logging.Logger:
    transports = get_transports(config)
    formatter = get_formatter(config)
    output_dir = get_output_dir(config)
    filename = get_filename(config)

    return compose(
        (
            set_file_transport(formatter, output_dir, filename)
            if "file" in transports
            else identity
        ),
        set_console_transport(formatter) if "console" in transports else identity,
    )


###


get_logger = lambda c, n=None: compose(
    set_transports(config=c),
    set_level(config=c),
    get_named_logger,
)(n)


__all__ = ["get_logger"]
