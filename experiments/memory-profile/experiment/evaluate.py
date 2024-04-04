import sys
import logging

from multiprocessing import Process, Pipe, connection
from common.logging import setup_logger
from common.data.synthetic import generate_and_save_for_range
from common.profilers.proc import (
    get_pid_status,
    get_peak_memory_usage_from_status,
)


def main(
    num_inlines_step: int,
    num_inlines_range_size: int,
    attributes: list[str],
    num_crosslines_and_samples: int,
    output_dir: str,
):
    logging.info("Starting experiment")

    datasets_dir = f"{output_dir}/data"
    dataset_paths = generate_and_save_for_range(
        num_inlines_step,
        num_inlines_range_size,
        num_crosslines_and_samples,
        num_crosslines_and_samples,
        datasets_dir,
    )
    supervisor_conn, worker_conn = Pipe()

    for attribute in attributes:
        logging.info(f"Executing experiment for attribute: {attribute}")
        for dataset_path in dataset_paths:
            worker_pid = __launch_worker(worker_conn, dataset_path, attribute)
            print(worker_pid)
    # For each attribute
    # Executes a new worker
    # The worker loads the dataset
    # Executes the attribute


def __launch_worker(
    conn: connection.Connection, dataset_path: str, attribute: str
) -> str:
    p = Process(target=__execute_experiment, args=(conn, dataset_path, attribute))
    p.start()

    return p.pid


def __execute_experiment(
    conn: connection.Connection,
    dataset_path: str,
    attribute: str,
) -> None:
    print("ok")


if __name__ == "__main__":
    num_inlines_step = int(sys.argv[1])
    num_inlines_range_size = int(sys.argv[2])
    attributes = sys.argv[3].split(",")
    num_crosslines_and_samples = int(sys.argv[4])
    output_dir = sys.argv[5]

    setup_logger("DEBUG")
    main(
        num_inlines_step,
        num_inlines_range_size,
        attributes,
        num_crosslines_and_samples,
        output_dir,
    )
