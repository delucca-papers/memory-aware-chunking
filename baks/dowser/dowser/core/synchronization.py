import time

from typing import Callable, Any
from threading import Event
from multiprocessing import Queue
from functools import wraps
from dowser.logger import get_logger


def queue_to_list(queue: Queue) -> list[Any]:
    return [queue.get() for _ in range(queue.qsize())]


def hook_sync_event(function: Callable, sync_event: Event) -> Callable:
    logger = get_logger()
    logger.info(f'Hooking sync event to function "{function.__name__}"')

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        logger.info(f'Executing function "{function.__name__}"')
        result = function(*args, **kwargs)
        sync_event.set()

        return result

    return wrapper


def loop_until_sync(
    function: Callable,
    sync_event: Event,
    queue: Queue,
    precision: float,
    *args,
    **kwargs,
) -> None:
    while not sync_event.is_set():
        iteration_result = function(*args, **kwargs)
        queue.put(iteration_result)

        time.sleep(precision)

    return


__alL__ = ["hook_sync_event", "loop_until_sync", "queue_to_list"]
