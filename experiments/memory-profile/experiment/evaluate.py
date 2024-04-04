import sys
import logging

from multiprocessing import Process, Pipe, connection
from common.logging import setup_logger
from common.constants import (
    STARTED_EXPERIMENT,
    LOADED_DATASET,
    EXECUTED_ATTRIBUTE,
    FINISHED_EXPERIMENT,
)
from common.watchers import watch_memory_usage
from common.data.synthetic import generate_and_save_for_range
from common.data.loaders import load_segy


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
            watch_memory_usage(
                worker_pid,
                supervisor_conn,
                output_dir,
            )


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
    conn.send(STARTED_EXPERIMENT)
    conn.recv()

    data = load_segy(dataset_path)
    conn.send(LOADED_DATASET)
    conn.recv()

    conn.send(FINISHED_EXPERIMENT)


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
