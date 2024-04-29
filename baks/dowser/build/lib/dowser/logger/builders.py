from logging import Logger
from toolz import compose, memoize
from .transports import set_transports
from .context import logger_context


def __set_level(logger: Logger) -> Logger:
    logger.setLevel(logger_context.level)
    return logger


build_logger = memoize(
    compose(
        set_transports,
        __set_level,
    ),
)


__all__ = ["build_logger"]
