import os

from multiprocessing import Process, Manager
from common.transformers import dataset_path_to_name
from common.logging import setup_logger, get_module_logger
from common.events import EventName, EventDispatcher
from common.watchers.memory_usage import watch_memory_usage
from common.watchers.execution_time import watch_execution_time
from common.executors import execute_attribute
from common.data.synthetic import generate_and_save_for_range

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

    dataset_path_list, event_dispatcher, watcher_results = __initialize(
        num_inlines,
        num_crosslines,
        num_samples,
        output_dir,
    )

    for attribute in attributes:
        module_logger.info(f"Executing experiment for attribute: {attribute}")
        for dataset_path in dataset_path_list:
            for iteration_num in range(num_iterations):
                worker_id = __build_worker(
                    attribute,
                    dataset_path,
                    event_dispatcher,
                )
                watchers = __build_watchers(
                    worker_id,
                    watcher_results,
                    event_dispatcher,
                )

                for watcher in watchers:
                    watcher.join()

                __save_reports(
                    watcher_results,
                    dataset_path,
                    attribute,
                    output_dir,
                    iteration_num + 1,  # Since iteration_num starts from 0
                )

                __reset(watcher_results, event_dispatcher)


def __build_watchers(
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


def __build_worker(
    attribute: str,
    dataset_path: str,
    event_dispatcher: EventDispatcher,
) -> str:
    worker = Process(
        target=execute_attribute,
        args=(
            attribute,
            dataset_path,
            event_dispatcher,
        ),
    )

    worker.start()

    return worker.pid


def __initialize(
    num_inlines: int,
    num_crosslines: int,
    num_samples: int,
    output_dir: str,
) -> tuple[list[str], EventDispatcher, dict]:
    manager = Manager()
    watcher_results = manager.dict()
    watcher_results["memory_usage"] = []
    watcher_results["execution_time"] = []

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


def __reset(watcher_results: dict, event_dispatcher: EventDispatcher) -> None:
    event_dispatcher.reset()
    watcher_results["memory_usage"] = []
    watcher_results["execution_time"] = []


def __save_reports(
    watcher_results: dict,
    dataset_path: str,
    attribute_name: str,
    output_dir: str,
    iteration_num: int,
) -> None:
    dataset_name = dataset_path_to_name(dataset_path)
    reports_dir = os.path.join(output_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    __save_memory_usage_report(
        watcher_results,
        attribute_name,
        iteration_num,
        dataset_name,
        reports_dir,
    )

    __save_execution_time_report(
        watcher_results,
        attribute_name,
        iteration_num,
        dataset_name,
        reports_dir,
    )


def __save_memory_usage_report(
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
    module_logger.debug(f"Memory usage: {watcher_results['memory_usage']}")

    with open(report_filepath, "a") as f:
        for event, memory_usage in watcher_results["memory_usage"]:
            f.write(
                f"{attribute_name},{dataset_name},{iteration_num},{event},{memory_usage}\n"
            )


def __save_execution_time_report(
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
    module_logger.debug(f"Execution time: {watcher_results['execution_time']}")

    with open(report_filepath, "a") as f:
        for event, execution_time in watcher_results["execution_time"]:
            f.write(
                f"{attribute_name},{dataset_name},{iteration_num},{event},{execution_time}\n"
            )


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
