import sys
import logging

from multiprocessing import Process, Pipe, connection
from common.transformers import dataset_path_to_name
from common.logging import setup_logger
from common.watchers import (
    watch_memory_usage,
    build_event_dispatcher,
    monitor_attribute,
)
from common.data.synthetic import generate_and_save_for_range


def main(
    num_inlines_step: int,
    num_inlines_range_size: int,
    attributes: list[str],
    num_crosslines_and_samples: int,
    output_dir: str,
    num_iterations_per_inline: int,
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
    dispatch_event = build_event_dispatcher(worker_conn)

    for attribute in attributes:
        logging.info(f"Executing experiment for attribute: {attribute}")
        for dataset_path in dataset_paths:
            dataset_name = dataset_path_to_name(dataset_path)
            for iteration_num in range(num_iterations_per_inline):
                worker_pid = __launch_worker(dispatch_event, dataset_path, attribute)
                watch_memory_usage(
                    worker_pid,
                    supervisor_conn,
                    attribute,
                    dataset_name,
                    output_dir,
                    iteration_num + 1,  # Since it starts at 0
                )


def __launch_worker(
    conn: connection.Connection, dataset_path: str, attribute: str
) -> str:
    p = Process(target=monitor_attribute, args=(conn, dataset_path, attribute))
    p.start()

    return p.pid


if __name__ == "__main__":
    num_inlines_step = int(sys.argv[1])
    num_inlines_range_size = int(sys.argv[2])
    attributes = sys.argv[3].split(",")
    num_crosslines_and_samples = int(sys.argv[4])
    output_dir = sys.argv[5]
    num_iterations_per_inline = int(sys.argv[6])

    setup_logger()
    main(
        num_inlines_step,
        num_inlines_range_size,
        attributes,
        num_crosslines_and_samples,
        output_dir,
        num_iterations_per_inline,
    )
