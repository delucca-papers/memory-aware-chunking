import os

from multiprocessing import Process
from common.logging import setup_logger, get_module_logger
from common.events import EventName, EventDispatcher
from common.executors import build_executor_worker
from common.data.synthetic import generate_and_save_for_range
from common.watchers import (
    build_all_watchers,
    save_reports,
    reset_watcher_results,
    initialize_watcher_requirements,
)


module_logger = get_module_logger()


def main(
    num_inlines: int,
    num_crosslines: int,
    num_samples: int,
    step_size: int,
    range_size: int,
    num_iterations: int,
    attributes: list[str],
    output_dir: str,
):
    module_logger.info("Starting experiment")

    dataset_path_list, event_dispatcher, watcher_results = __initialize(
        num_inlines,
        num_crosslines,
        num_samples,
        step_size,
        range_size,
        output_dir,
    )

    for attribute in attributes:
        module_logger.info(f"Executing experiment for attribute: {attribute}")
        for dataset_path in dataset_path_list:
            for iteration_num in range(num_iterations):
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

                save_reports(
                    watcher_results,
                    dataset_path,
                    attribute,
                    output_dir,
                    iteration_num + 1,  # Since iteration_num starts from 0
                )

                reset_watcher_results(watcher_results, event_dispatcher)


def __initialize(
    num_inlines: int,
    num_crosslines: int,
    num_samples: int,
    step_size: int,
    range_size: int,
    output_dir: str,
) -> tuple[list[str], EventDispatcher, dict]:
    watcher_results = initialize_watcher_requirements()

    event_dispatcher = EventDispatcher(
        barrier_event_names=[
            EventName.MEASURED_MEMORY_USAGE,
            EventName.MEASURED_EXECUTION_TIME,
        ]
    )

    data_dir = f"{output_dir}/data"
    dataset_paths = generate_and_save_for_range(
        num_inlines,
        num_crosslines,
        num_samples,
        step_size,
        range_size,
        data_dir,
    )

    return dataset_paths, event_dispatcher, watcher_results


if __name__ == "__main__":
    num_inlines = int(os.environ.get("NUM_INLINES"))
    num_crosslines = int(os.environ.get("NUM_CROSSLINES"))
    num_samples = int(os.environ.get("NUM_SAMPLES"))
    step_size = int(os.environ.get("STEP_SIZE"))
    range_size = int(os.environ.get("RANGE_SIZE"))
    num_iterations = int(os.environ.get("NUM_ITERATIONS"))
    attributes = os.environ.get("ATTRIBUTES").split(",")
    output_dir = os.environ.get("OUTPUT_DIR")
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    setup_logger(log_level)
    main(
        num_inlines,
        num_crosslines,
        num_samples,
        step_size,
        range_size,
        num_iterations,
        attributes,
        output_dir,
    )
