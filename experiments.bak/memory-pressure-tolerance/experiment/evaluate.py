import os
import psutil

from common.logging import setup_logger, get_module_logger
from common.events import EventName, EventDispatcher
from common.executors import build_executor_worker
from common.data.synthetic import generate_and_save_synthetic_data
from common.cgroup import set_memory_limit_for_pid
from common.handlers import wait_for_all
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
    cgroup_name: str,
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

            worker = build_executor_worker(
                attribute,
                dataset_path,
                event_dispatcher,
            )

            __limit_worker_memory(
                cgroup_name,
                worker.pid,
                99.9999,
                maximum_memory_usage,
            )

            watchers = build_all_watchers(
                worker.pid,
                watcher_results,
                event_dispatcher,
            )

            wait_for_all(worker, watchers, event_dispatcher)

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

    worker = build_executor_worker(
        attribute,
        dataset_path,
        event_dispatcher,
    )

    watchers = build_all_watchers(
        worker.pid,
        watcher_results,
        event_dispatcher,
    )

    wait_for_all(worker, watchers, event_dispatcher)

    peak_memory_used = get_peak_memory_used(watcher_results)
    reset_watcher_results(watcher_results, event_dispatcher)

    module_logger.debug(f"Peak memory used: {peak_memory_used}")

    return peak_memory_used


def __limit_worker_memory(
    cgroup_name: str,
    worker_pid: str,
    memory_pressure: int,
    profiled_memory_usage: int,
) -> None:
    module_logger.debug(f"Memory pressure: {memory_pressure}%")
    module_logger.debug(f"Profiled memory usage: {profiled_memory_usage} kB")
    module_logger.debug(f"Worker PID: {worker_pid}")

    allowed_memory_pct = (100 - memory_pressure) / 100
    maximum_memory_in_kb = int(allowed_memory_pct * profiled_memory_usage)
    module_logger.info(f"Setting maximum memory usage to {maximum_memory_in_kb} kB")
    maximum_memory_in_bytes = maximum_memory_in_kb * 1024

    set_memory_limit_for_pid(cgroup_name, worker_pid, maximum_memory_in_bytes)


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
    cgroup_name = os.environ.get("CGROUP_NAME")
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
        cgroup_name,
        output_dir,
    )
