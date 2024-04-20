from typing import Callable, Any
from .core import get_logger, config

get_num_iterations = config.lazy_get("model.collect.num_iterations", type=int)


def collect_profile(
    function: Callable,
    inputs: list[Any],
    input_handler: Callable | None = None,
):
    num_iterations = get_num_iterations()

    logger = get_logger()
    logger.info(
        f'Collecting profile for function "{function.__name__}" from "{function.__module__}"'
    )
    logger.info(f"Number of inputs to build model: {len(inputs)}")
    logger.debug(f"Number of iterations: {num_iterations}")
    logger.debug(
        f'Input handler: "{input_handler.__name__}" from "{input_handler.__module__}"'
    )


__all__ = ["collect_profile"]
