from typing import Callable, Any
from multiprocessing import Queue
from threading import Event, Thread
from toolz import curry
from dowser.logger import get_logger
from dowser.common import lazy
from .synchronization import loop_until_sync, queue_to_list


def get_result(thread: Thread, queue: Queue) -> list[Any]:
    thread.join()
    return queue_to_list(queue)


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

    queue = Queue()
    sync_event = Event()
    thread = Thread(
        target=loop_until_sync,
        args=(function, sync_event, queue, precision, *args),
        kwargs=kwargs,
    )
    thread.start()

    result_handler = lazy(get_result)(thread, queue)

    return result_handler, sync_event


__all__ = ["parallelized_profiler"]
