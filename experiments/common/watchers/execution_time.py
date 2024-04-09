from time import time
from typing import Callable
from ..events import EventDispatcher, EventName
from ..logging import get_module_logger

module_logger = get_module_logger()


def watch_execution_time(
    event_dispatcher: EventDispatcher,
    watcher_results: dict,
    key: str = "execution_time",
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
