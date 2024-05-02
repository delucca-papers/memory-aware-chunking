import inspect

from typing import Callable
from toolz import compose, curry, do
from .config import Config
from .common.transformers import deep_merge
from .common.logger import setup_logger_from_config, logger
from .profiler import run_profiler


__all__ = ["load_config", "get_logger", "profile", "context"]


class Context:
    config: Config = compose(
        curry(do)(setup_logger_from_config),
        Config.from_initial_config,
    )()


context = Context()


def load_config(config: dict) -> None:
    old_config = context.config.model_dump()
    new_config = deep_merge(old_config, config, append=False)

    context.config = Config(**new_config)

    if "logger" in config:
        setup_logger_from_config(context.config)


def profile(function: Callable, *args, **kwargs) -> None:
    function_filepath = inspect.getfile(function)
    function_name = function.__name__

    config = {
        "profiler": {
            "filepath": function_filepath,
            "entrypoint": function_name,
            "args": args,
            "kwargs": kwargs,
        }
    }
    load_config(config)

    run_profiler(context.config)


def get_logger():
    return logger
