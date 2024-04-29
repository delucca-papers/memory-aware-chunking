import os
import sys

from loguru import logger
from toolz import compose, do, curry
from .config import Config
from .builders import isonow


__all__ = ["logger", "setup_logger_from_config"]


def clear_handlers(_: Config) -> None:
    logger.remove()


def set_transports(config: Config) -> None:
    available_transports = {
        "console": set_console_transport,
        "file": set_file_transport,
    }

    for transport in config.get("logger.enabled_transports"):
        transport_handler = available_transports.get(transport)
        if not transport_handler:
            raise ValueError(f'Invalid logger handler: "{transport}"')

        transport_handler(config)


def set_console_transport(config: Config) -> None:
    logger.add(sys.stdout, level=config.get("logger.level").upper())


def set_file_transport(config: Config) -> None:
    now = isonow()
    filename = f"{now}.log"
    filepath = os.path.join(config.get("output_dir"), filename)
    logger.add(filepath, level=config.get("logger.level").upper())


setup_logger_from_config = compose(
    curry(do)(set_transports),
    curry(do)(clear_handlers),
)
