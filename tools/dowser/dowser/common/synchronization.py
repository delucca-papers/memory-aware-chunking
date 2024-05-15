from typing import Callable
from functools import wraps
from multiprocessing import Process


__all__ = ["lazy", "passthrough", "run_subprocess"]


def lazy(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        @wraps(func)
        def delayed():
            return func(*args, **kwargs)

        return delayed

    return wrapper


def passthrough(*args, **kwargs):
    return args, kwargs


def run_subprocess(
    target: Callable,
    *target_args,
    sync: bool = False,
    **target_kwargs,
) -> Process:
    process = Process(target=target, args=target_args, kwargs=target_kwargs)

    process.start()

    if sync:
        process.join()

    return process
