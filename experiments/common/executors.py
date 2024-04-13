import importlib

from multiprocessing import Process
from typing import Callable
from .events import EventName, EventDispatcher
from .data.loaders import load_segy


def execute_attribute(
    attribute: str,
    dataset_path: str,
    event_dispatcher: EventDispatcher,
) -> None:
    event_dispatcher.wait_watchers_start()
    event_dispatcher.dispatch(EventName.STARTED_EXPERIMENT, sync=True)

    data = load_segy(dataset_path)
    event_dispatcher.dispatch(EventName.LOADED_DATASET, sync=True)

    attribute_module = importlib.import_module(
        f".attributes.{attribute}",
        package="common",
    )
    attribute_func = getattr(attribute_module, "run")
    attribute_func(data)
    event_dispatcher.dispatch(EventName.EXECUTED_ATTRIBUTE, sync=True)

    event_dispatcher.dispatch(EventName.FINISHED_EXPERIMENT)


def build_executor_worker(
    attribute: str,
    dataset_path: str,
    event_dispatcher: EventDispatcher,
    target_function: Callable[[str, str, EventDispatcher], None] = execute_attribute,
) -> str:
    worker = Process(
        target=target_function,
        args=(
            attribute,
            dataset_path,
            event_dispatcher,
        ),
    )

    worker.start()

    return worker.pid
