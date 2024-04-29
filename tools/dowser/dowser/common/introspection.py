import inspect


__all__ = ["get_function_path"]


def get_function_path(function: callable) -> str:
    return f"{function.__module__}.{function.__name__}"
