from typing import Callable, Any
from threading import Event, Thread
from toolz import curry
from multiprocessing import Queue
from dowser.logger import get_logger
from dowser.common import lazy
from .synchronization import loop_until_sync, queue_to_list


def get_result(thread: Thread, profile: Queue) -> list[Any]:
    thread.join()
    return queue_to_list(profile)


@curry
def parallelized_profiler(
    function: Callable,
    precision: float,
    *args,
    **kwargs,
) -> tuple[Callable, Event]:
    logger = get_logger()
    logger.debug(
        f"Setting up threading parallelized profiler for function {function.__name__}"
    )

    sync_event = Event()
    profile = Queue()

    thread = Thread(
        target=loop_until_sync,
        args=(function, sync_event, profile, precision, *args),
        kwargs=kwargs,
    )
    thread.start()

    result_handler = lazy(get_result)(thread, profile)

    return result_handler, sync_event


__all__ = ["parallelized_profiler"]
