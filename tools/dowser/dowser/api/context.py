from toolz import compose, curry, do
from dowser.config import Config
from dowser.common.logger import setup_logger_from_config


__all__ = ["context"]


class Context:
    config: Config = compose(
        curry(do)(setup_logger_from_config),
        Config.from_initial_config,
    )()


context = Context()
