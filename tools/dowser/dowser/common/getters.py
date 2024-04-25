import inspect

from typing import Callable


def __get_defined_function_path(function: Callable) -> str:
    return f"{function.__module__}.{function.__name__}"


def __get_caller_function_path() -> str:
    stack = inspect.stack()
    caller_frame = stack[2]
    module = inspect.getmodule(caller_frame[0])
    module_name = module.__name__
    function_name = caller_frame[3]

    return f"{module_name}.{function_name}"


def get_function_path(function: Callable | None = None) -> str:
    return (
        __get_defined_function_path(function)
        if function
        else __get_caller_function_path()
    )


__all__ = ["get_function_path"]
