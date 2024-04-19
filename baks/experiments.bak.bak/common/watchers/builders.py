from multiprocessing import Process, Manager
from ..events import EventDispatcher
from .memory_usage import watch_memory_usage
from .execution_time import watch_execution_time
from .constants import (
    MEMORY_USAGE_RESULTS_NAME,
    EXECUTION_TIME_RESULTS_NAME,
)


def build_all_watchers(
    worker_pid: str,
    watcher_results: dict,
    event_dispatcher: EventDispatcher,
) -> list[Process]:
    mem_usage_watcher = Process(
        target=watch_memory_usage,
        args=(
            event_dispatcher,
            worker_pid,
            watcher_results,
        ),
    )
    execution_time_watcher = Process(
        target=watch_execution_time,
        args=(
            event_dispatcher,
            watcher_results,
        ),
    )

    mem_usage_watcher.start()
    execution_time_watcher.start()

    return [mem_usage_watcher, execution_time_watcher]


def initialize_watcher_requirements() -> dict:
    manager = Manager()
    watcher_results = manager.dict()
    watcher_results[MEMORY_USAGE_RESULTS_NAME] = []
    watcher_results[EXECUTION_TIME_RESULTS_NAME] = []

    return watcher_results
