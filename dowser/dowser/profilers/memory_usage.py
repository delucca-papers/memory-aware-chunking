from typing import Callable, Any
from logging import Logger
from functools import wraps
from toolz import compose
from threading import Event, Thread
from queue import Queue
from ..config import config, get_namespace, get_config
from ..logging import get_logger

get_profiler_config = lambda c: get_namespace("profiler", c)
get_memory_usage_profiler_config = lambda c: get_namespace("memory_usage", c)
get_backend_name = lambda c: compose(
    lambda c: get_config("backend", c),
    get_memory_usage_profiler_config,
    get_profiler_config,
)(c)


###


def with_backend(config: dict, function: Callable) -> Any:
    logger = get_logger()
    backend_name = get_backend_name(config)
    logger.debug(f'Executing message usage profiler with "{backend_name}" backend')

    backend_wrapper = globals().get(f"with_{backend_name}_backend")
    if backend_wrapper is None:
        logger.error(f'Backend "{backend_name}" is not implemented yet')
        return

    return backend_wrapper(config, function)


def with_kernel_backend(config: dict, function: Callable):
    logger = get_logger()

    @wraps(function)
    def wrapped_function(*args, **kwargs):
        threaded_data = with_threaded_profiler(kernel_profiler_thread, config)
        function_results = function(*args, **kwargs)
        profiler_results = with_profiler_results(*threaded_data)

        logger.debug(f"Profiler results: {profiler_results}")

        return function_results

    return wrapped_function


def kernel_profiler_thread(config: dict, event: Event, queue: Queue) -> list[float]:
    logger = get_logger()
    logger.info(f"Profiling memory usage with kernel backend")

    queue.put("ok")


def with_threaded_profiler(
    target_function: Callable,
    config: dict,
) -> tuple[Thread, Event, Queue]:
    logger = get_logger()
    logger.debug(
        f'Launching threaded profiler with function "{target_function.__name__}"'
    )

    event = Event()
    queue = Queue()
    thread = Thread(target=target_function, args=(config, event, queue))
    thread.start()

    return thread, event, queue


def with_profiler_results(thread: Thread, event: Event, queue: Queue) -> list[float]:
    logger = get_logger()
    logger.debug(f"Fetching profiler results")

    event.set()
    thread.join()

    return [queue.get() for _ in range(queue.qsize())]


###


def profile(config: dict = config) -> Callable:
    logger = get_logger()
    def decorator(function: Callable):
        logger.debug(
            f'Setting up memory usage profiler for function "{function.__name__}"'
        )

        return with_backend(config, function)

    return decorator


__all__ = ["profile"]
