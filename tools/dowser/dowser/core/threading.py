from threading import Event, Thread
from queue import Queue
from typing import Callable, Any
from functools import wraps
from .logging import get_logger
from .types import ThreadWrapper, ThreadWrappedResult


def start_thread(function: Callable, *args, **kwargs) -> Thread:
    logger = get_logger()
    logger.debug(f'Launching function "{function.__name__}" in a separate thread')

    thread = Thread(target=function, args=args, kwargs=kwargs)
    thread.start()

    return thread


def start_event_controlled_thread(
    function: Callable,
    *args,
    **kwargs,
) -> tuple[Thread, Event, Queue]:
    event = Event()
    queue = Queue()
    thread = start_thread(function, event, queue, *args, **kwargs)

    return thread, event, queue


def finish_event_controlled_thread(
    thread: Thread,
    event: Event,
    queue: Queue,
) -> list[Any]:
    logger = get_logger()
    logger.debug(f"Finishing and fetching results for thread {thread.ident}")

    event.set()
    thread.join()

    return [queue.get() for _ in range(queue.qsize())]


###


def threaded_wrapper(
    function: Callable,
    thread_function: Callable,
    *thread_args,
    **thread_kwargs,
) -> ThreadWrapper:
    logger = get_logger()

    @wraps(function)
    def wrapped_function(*args, **kwargs) -> ThreadWrappedResult:
        thread, event, queue = start_event_controlled_thread(
            thread_function,
            *thread_args,
            **thread_kwargs,
        )
        logger.info(f"Using thread {thread.ident} as wrapper")

        function_results = function(*args, **kwargs)
        profiler_results = finish_event_controlled_thread(thread, event, queue)

        return profiler_results, function_results

    return wrapped_function


__all__ = ["threaded_wrapper"]
