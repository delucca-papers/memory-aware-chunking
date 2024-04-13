import os

from time import time
from typing import Callable
from ..events import EventDispatcher, EventName
from ..logging import get_module_logger
from .constants import EXECUTION_TIME_RESULTS_NAME

module_logger = get_module_logger()


def save_execution_time_report(
    watcher_results: dict,
    attribute_name: str,
    iteration_num: int,
    dataset_name: str,
    output_dir: str,
    filename: str = "execution_time_report.csv",
) -> None:
    report_filepath = os.path.join(output_dir, filename)
    if not os.path.exists(report_filepath):
        with open(report_filepath, "w") as f:
            f.write(
                "Attribute,Dataset Shape,Iteration,Event,Time Since Epoch (in seconds)\n"
            )

    module_logger.debug(f"Saving execution time report for {dataset_name}")
    module_logger.debug(
        f"Execution time: {watcher_results[EXECUTION_TIME_RESULTS_NAME]}"
    )

    with open(report_filepath, "a") as f:
        for event, execution_time in watcher_results[EXECUTION_TIME_RESULTS_NAME]:
            f.write(
                f"{attribute_name},{dataset_name},{iteration_num},{event},{execution_time}\n"
            )


def watch_execution_time(
    event_dispatcher: EventDispatcher,
    watcher_results: dict,
    key: str = EXECUTION_TIME_RESULTS_NAME,
) -> None:
    measure_time_for_event = __build_event_time_measurer(event_dispatcher)
    event_dispatcher.dispatch(EventName.STARTED_EXECUTION_TIME_WATCHER)

    started_experiment_time = measure_time_for_event(EventName.STARTED_EXPERIMENT)
    loaded_dataset_time = measure_time_for_event(EventName.LOADED_DATASET)
    executed_attribute_time = measure_time_for_event(EventName.EXECUTED_ATTRIBUTE)

    watcher_results[key] = [
        ("STARTED_EXPERIMENT", started_experiment_time),
        ("LOADED_DATASET", loaded_dataset_time),
        ("EXECUTED_ATTRIBUTE", executed_attribute_time),
    ]


def __build_event_time_measurer(
    event_dispatcher: EventDispatcher,
) -> Callable[[EventName], float]:
    def event_time_measurer(next_event_name: EventName) -> float:
        module_logger.debug(f"Measuring time for {next_event_name}")
        event_dispatcher.wait(next_event_name)

        measured_time = time()
        module_logger.debug(f"Measured time for {next_event_name}: {measured_time}")
        event_dispatcher.dispatch(EventName.MEASURED_EXECUTION_TIME)

        return measured_time

    return event_time_measurer
