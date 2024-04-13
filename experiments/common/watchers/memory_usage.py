import os

from ..logging import get_module_logger
from ..events import EventName, EventDispatcher
from ..profilers.proc import (
    get_pid_status,
    get_peak_memory_usage_from_status,
    get_current_memory_usage_from_status,
)
from .constants import MEMORY_USAGE_RESULTS_NAME

module_logger = get_module_logger()


def save_memory_usage_report(
    watcher_results: dict,
    attribute_name: str,
    iteration_num: int,
    dataset_name: str,
    output_dir: str,
    filename: str = "memory_usage_report.csv",
) -> None:
    report_filepath = os.path.join(output_dir, filename)
    if not os.path.exists(report_filepath):
        with open(report_filepath, "w") as f:
            f.write("Attribute,Dataset Shape,Iteration,Event,Memory Usage (kB)\n")

    module_logger.debug(f"Saving memory usage report for {dataset_name}")
    module_logger.debug(f"Memory usage: {watcher_results[MEMORY_USAGE_RESULTS_NAME]}")

    with open(report_filepath, "a") as f:
        for event, memory_usage in watcher_results[MEMORY_USAGE_RESULTS_NAME]:
            f.write(
                f"{attribute_name},{dataset_name},{iteration_num},{event},{memory_usage}\n"
            )


def watch_memory_usage(
    event_dispatcher: EventDispatcher,
    pid: str,
    watcher_results: dict,
    key: str = MEMORY_USAGE_RESULTS_NAME,
) -> None:
    next_event = event_dispatcher.get_next(
        [
            EventName.STARTED_EXPERIMENT,
            EventName.LOADED_DATASET,
            EventName.EXECUTED_ATTRIBUTE,
        ]
    )

    is_watcher_started = event_dispatcher.is_event_set(
        EventName.STARTED_MEMORY_USAGE_WATCHER
    )
    if not is_watcher_started:
        event_dispatcher.dispatch(EventName.STARTED_MEMORY_USAGE_WATCHER)

    if not next_event:
        module_logger.debug("Finished experiment")
        return

    event_dispatcher.wait(next_event)
    module_logger.debug(f"Received event: {next_event.value}")

    event_memory_usage = __measure_memory_usage(next_event, pid)
    watcher_results[key] += [(next_event.value, event_memory_usage)]

    event_dispatcher.dispatch(EventName.MEASURED_MEMORY_USAGE)
    watch_memory_usage(
        event_dispatcher,
        pid,
        watcher_results,
        key,
    )


def __measure_memory_usage(event: EventName, pid: str) -> int:
    memory_handlers = {
        EventName.STARTED_EXPERIMENT: __measure_current_memory_usage,
        EventName.LOADED_DATASET: __measure_peak_memory_usage,
        EventName.EXECUTED_ATTRIBUTE: __measure_peak_memory_usage,
    }

    memory_handler = memory_handlers[event]
    memory_usage = memory_handler(pid)
    module_logger.debug(f"Memory usage: {memory_usage} for pid: {pid}")

    return memory_usage


def __measure_current_memory_usage(pid: str) -> int:
    module_logger.debug(f"Measuring current memory usage for pid: {pid}")

    status = get_pid_status(pid)
    return get_current_memory_usage_from_status(status)


def __measure_peak_memory_usage(pid: str) -> int:
    module_logger.debug(f"Measuring peak memory usage for pid: {pid}")

    status = get_pid_status(pid)
    return get_peak_memory_usage_from_status(status)
