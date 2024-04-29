import os

from logging import Logger, StreamHandler, Formatter
from logging.handlers import RotatingFileHandler
from toolz import compose, identity
from .context import logger_context


def __is_transport_enabled(transport: str) -> bool:
    return transport in logger_context.enabled_transports


def __get_formatter() -> Formatter:
    return Formatter(logger_context.format)


def set_console_transport(logger: Logger) -> Logger:
    formatter = __get_formatter()

    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def set_file_transport(logger: Logger) -> Logger:
    formatter = __get_formatter()

    log_output_dir = logger_context.transport_file_output_dir
    log_filepath = logger_context.transport_file_abspath

    os.makedirs(log_output_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_filepath,
        maxBytes=logger_context.transport_file_max_bytes,
        backupCount=logger_context.transport_file_backup_count,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


set_transports = compose(
    (set_file_transport if __is_transport_enabled("file") else identity),
    (set_console_transport if __is_transport_enabled("console") else identity),
)


__all__ = ["set_transports"]
