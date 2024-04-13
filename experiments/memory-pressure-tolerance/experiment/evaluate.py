import os
import resource

from multiprocessing import Process
from typing import Callable
from common.logging import setup_logger, get_module_logger
from common.events import EventName, EventDispatcher
from common.executors import build_executor_worker, execute_attribute
from common.data.synthetic import generate_and_save_synthetic_data
from common.watchers import (
    build_all_watchers,
    save_reports,
    reset_watcher_results,
    initialize_watcher_requirements,
    get_peak_memory_used,
)

module_logger = get_module_logger()


def main(
    num_inlines: int,
    num_crosslines: int,
    num_samples: int,
    starting_pressure: int,
    step_size: int,
    num_iterations: int,
    attributes: list[str],
    output_dir: str,
):
    module_logger.info("Starting experiment")

    dataset_path, event_dispatcher, watcher_results = __initialize(
        num_inlines,
        num_crosslines,
        num_samples,
        output_dir,
    )

    for attribute in attributes:
        module_logger.info(f"Executing experiment for attribute: {attribute}")
        for iteration_num in range(num_iterations):
            maximum_memory_usage = __profile_memory_used(
                attribute,
                dataset_path,
                event_dispatcher,
                watcher_results,
            )

            worker_id = build_executor_worker(
                attribute,
                dataset_path,
                event_dispatcher,
                target_function=__build_memory_pressure_executor(
                    starting_pressure,
                    maximum_memory_usage,
                ),
            )
            watchers = build_all_watchers(
                worker_id,
                watcher_results,
                event_dispatcher,
            )

            for watcher in watchers:
                watcher.join()

            save_reports(
                watcher_results,
                dataset_path,
                attribute,
                output_dir,
                iteration_num + 1,  # Since iteration_num starts from 0
            )

            reset_watcher_results(watcher_results, event_dispatcher)


def __profile_memory_used(
    attribute: str,
    dataset_path: str,
    event_dispatcher: EventDispatcher,
    watcher_results: dict,
) -> int:
    module_logger.info(f"Profiling memory usage for attribute {attribute}")

    worker_id = build_executor_worker(
        attribute,
        dataset_path,
        event_dispatcher,
    )

    watchers = build_all_watchers(
        worker_id,
        watcher_results,
        event_dispatcher,
    )

    for watcher in watchers:
        watcher.join()

    peak_memory_used = get_peak_memory_used(watcher_results)
    reset_watcher_results(watcher_results, event_dispatcher)

    module_logger.debug(f"Peak memory used: {peak_memory_used}")

    return peak_memory_used


def __build_memory_pressure_executor(
    memory_pressure: int,
    profiled_memory_usage: int,
) -> Callable[[str, str, EventDispatcher], None]:
    module_logger.debug(f"Memory pressure: {memory_pressure}%")
    module_logger.debug(f"Profiled memory usage: {profiled_memory_usage}")

    def executor(
        attribute: str,
        dataset_path: str,
        event_dispatcher: EventDispatcher,
    ) -> None:
        allowed_memory_pct = (100 - memory_pressure) / 100
        maximum_memory_in_kb = int(allowed_memory_pct * profiled_memory_usage)
        module_logger.info(f"Setting maximum memory usage to {maximum_memory_in_kb} kB")
        maximum_memory_in_bytes = maximum_memory_in_kb * 1024
        maximum_memory_in_bytes = int(profiled_memory_usage * 1024)

        resource.setrlimit(
            resource.RLIMIT_AS, (maximum_memory_in_bytes, resource.RLIM_INFINITY)
        )

        execute_attribute(attribute, dataset_path, event_dispatcher)

    return executor


def __initialize(
    num_inlines: int,
    num_crosslines: int,
    num_samples: int,
    output_dir: str,
) -> tuple[str, EventDispatcher, dict]:
    watcher_results = initialize_watcher_requirements()

    event_dispatcher = EventDispatcher(
        barrier_event_names=[
            EventName.MEASURED_MEMORY_USAGE,
            EventName.MEASURED_EXECUTION_TIME,
        ]
    )

    data_dir = f"{output_dir}/data"
    dataset_path = generate_and_save_synthetic_data(
        num_inlines,
        num_crosslines,
        num_samples,
        output_dir=data_dir,
    )

    return dataset_path, event_dispatcher, watcher_results


if __name__ == "__main__":
    num_inlines = int(os.environ.get("NUM_INLINES"))
    num_crosslines = int(os.environ.get("NUM_CROSSLINES"))
    num_samples = int(os.environ.get("NUM_SAMPLES"))
    starting_pressure = int(os.environ.get("STARTING_PRESSURE"))
    step_size = int(os.environ.get("STEP_SIZE"))
    num_iterations = int(os.environ.get("NUM_ITERATIONS"))
    attributes = os.environ.get("ATTRIBUTES").split(",")
    output_dir = os.environ.get("OUTPUT_DIR")
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    setup_logger(log_level)
    main(
        num_inlines,
        num_crosslines,
        num_samples,
        starting_pressure,
        step_size,
        num_iterations,
        attributes,
        output_dir,
    )
