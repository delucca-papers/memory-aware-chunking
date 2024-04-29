import inspect

from typing import Callable
from .transformers import args_to_str


def get_defined_function_path(function: Callable) -> str:
    return f"{function.__module__}.{function.__name__}"


def get_caller_function_path() -> str:
    stack = inspect.stack()
    caller_frame = stack[2]
    module = inspect.getmodule(caller_frame[0])
    module_name = module.__name__
    function_name = caller_frame[3]

    return f"{module_name}.{function_name}"


def get_function_path(function: Callable | None = None) -> str:
    return (
        get_defined_function_path(function) if function else get_caller_function_path()
    )


def get_function_inputs(function: Callable, args: tuple, kwargs: dict) -> str:
    function_signature = inspect.signature(function)
    binded_signature = function_signature.bind(*args, **kwargs)
    binded_signature.apply_defaults()
    called_args = binded_signature.arguments

    return args_to_str(called_args)


__all__ = ["get_function_path", "get_function_inputs", "start_tracer", "stop_tracer"]
