from typing import Callable
from functools import wraps
from dowser.logger import get_logger
from dowser.common import Report, get_function_path, get_function_inputs
from .metrics import build_enabled_profilers
from .report import ProfilerReport


def profile(function: Callable):
    logger = get_logger()
    logger.info(f'Setting up profilers for function "{function.__name__}"')

    report = ProfilerReport()
    with_enabled_profilers = build_enabled_profilers(report)
    function_metadata = {
        "function_path": get_function_path(function),
    }

    @wraps(function)
    def wrapper(*args, **kwargs):
        logger.info(f'Profiling function "{function.__name__}"')

        execution_metadata = {
            **function_metadata,
            "inputs": get_function_inputs(function, args, kwargs),
        }
        profiled_function = with_enabled_profilers(execution_metadata, function)

        result = profiled_function(*args, **kwargs)

        report.save()

        return result

    return wrapper


__all__ = ["profile"]
