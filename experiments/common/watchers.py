import logging
import importlib
import os

from multiprocessing import connection
from .types import EventDispatcher
from .constants import (
    STARTED_EXPERIMENT,
    LOADED_DATASET,
    EXECUTED_ATTRIBUTE,
    FINISHED_EXPERIMENT,
    SUPERVISOR_RESPONSE,
)
from .profilers.proc import (
    get_pid_status,
    get_peak_memory_usage_from_status,
    get_current_memory_usage_from_status,
)
from .data.loaders import load_segy


def build_event_dispatcher(conn: connection.Connection) -> EventDispatcher:
    def dispatch_event(event: str) -> None:
        conn.send(event)
        if event != FINISHED_EXPERIMENT:
            conn.recv()

    return dispatch_event


def monitor_attribute(
    dispatch_event: EventDispatcher,
    dataset_path: str,
    attribute: str,
) -> None:
    dispatch_event(STARTED_EXPERIMENT)

    data = load_segy(dataset_path)
    dispatch_event(LOADED_DATASET)

    attribute_module = importlib.import_module(
        f".attributes.{attribute}",
        package="common",
    )
    attribute_func = getattr(attribute_module, "run")
    attribute_func(data)
    dispatch_event(EXECUTED_ATTRIBUTE)

    dispatch_event(FINISHED_EXPERIMENT)


def watch_memory_usage(
    pid: str,
    conn: connection.Connection,
    attribute_name: str,
    dataset_name: str,
    output_dir: str,
    iteration_num: int = 1,
) -> None:
    event = conn.recv()
    logging.debug(f"Received event: {event}")

    if event == STARTED_EXPERIMENT:
        logging.info(f"Started experiment for dataset: {dataset_name}")

    if event != FINISHED_EXPERIMENT:
        __measure_memory_usage(
            event,
            pid,
            attribute_name,
            dataset_name,
            output_dir,
            conn,
            iteration_num,
        )


def __measure_memory_usage(
    event: str,
    pid: str,
    attribute_name: str,
    dataset_name: str,
    output_dir: str,
    conn: connection.Connection,
    iteration_num: int,
) -> None:
    memory_handlers = {
        STARTED_EXPERIMENT: __measure_current_memory_usage,
        LOADED_DATASET: __measure_peak_memory_usage,
        EXECUTED_ATTRIBUTE: __measure_peak_memory_usage,
    }

    memory_handler = memory_handlers[event]
    memory_usage = memory_handler(pid)
    logging.debug(f"Memory usage: {memory_usage} for pid: {pid}")

    __save_report(
        memory_usage,
        event,
        attribute_name,
        dataset_name,
        output_dir,
        iteration_num,
    )

    conn.send(SUPERVISOR_RESPONSE)
    watch_memory_usage(
        pid,
        conn,
        attribute_name,
        dataset_name,
        output_dir,
        iteration_num,
    )


def __measure_current_memory_usage(pid: str) -> int:
    logging.debug(f"Measuring current memory usage for pid: {pid}")

    status = get_pid_status(pid)
    return get_current_memory_usage_from_status(status)


def __measure_peak_memory_usage(pid: str) -> int:
    logging.debug(f"Measuring peak memory usage for pid: {pid}")

    status = get_pid_status(pid)
    return get_peak_memory_usage_from_status(status)


def __save_report(
    memory_usage: int,
    event: str,
    attribute_name: str,
    dataset_name: str,
    output_dir: str,
    iteration_num: int,
    filename: str = "memory_usage_report.csv",
) -> None:
    report_filepath = os.path.join(output_dir, filename)
    if not os.path.exists(report_filepath):
        with open(report_filepath, "w") as f:
            f.write("Attribute,Dataset Shape,Iteration,Event,Memory Usage (kB)\n")

    with open(report_filepath, "a") as f:
        f.write(
            f"{attribute_name},{dataset_name},{iteration_num},{event},{memory_usage}\n"
        )
