from typing import Callable, Any
from .core import get_logger
from .profile import profile
from .contexts import config, report_context

get_num_iterations = config.lazy_get("model.collect.num_iterations", type=int)


###


def collect_profile(
    function: Callable,
    inputs: list[Any],
    input_handler: Callable | None = None,
    group_name: str | None = None,
):
    num_iterations = get_num_iterations()
    group_name = group_name or function.__name__

    logger = get_logger()
    logger.info(
        f'Collecting profile for function "{function.__name__}" from "{function.__module__}"'
    )
    logger.info(f"Number of inputs to build model: {len(inputs)}")
    logger.debug(f"Number of iterations: {num_iterations}")
    logger.debug(
        f'Input handler: "{input_handler.__name__}" from "{input_handler.__module__}"'
    )

    report_context.update({"group": group_name})

    @profile
    def profiled_function(input_data: Any):
        input_data = input_handler(input_data) if input_handler else input_data
        return function(input_data)

    for i in range(num_iterations):
        logger.debug(f"Iteration: {i + 1}")
        for input_data in inputs:
            profiled_function(input_data)

    logger.info(f'Profile collection for "{group_name}" completed')


__all__ = ["collect_profile"]
