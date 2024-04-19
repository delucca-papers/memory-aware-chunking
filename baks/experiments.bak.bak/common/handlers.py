from multiprocessing import Process

from .logging import get_module_logger
from .events import EventDispatcher, EventName

module_logger = get_module_logger()


def wait_for_all(
    worker: Process,
    watchers: list[Process],
    event_dispatcher: EventDispatcher,
) -> None:
    worker.join()

    if worker.exitcode != 0:
        module_logger.error(f"Worker exited with non-zero exit code: {worker.exitcode}")
        event_dispatcher.dispatch(EventName.EXITED)
    else:
        for watcher in watchers:
            watcher.join()
