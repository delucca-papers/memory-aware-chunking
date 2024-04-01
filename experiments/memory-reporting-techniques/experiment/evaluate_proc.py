import sys

from memory_consuming_task import consume_large_memory
from common.transformers import kib_to_mib
from common.profilers.proc import (
    get_self_status,
    get_current_memory_usage_from_status,
    get_peak_memory_usage_from_status,
)

DEFAULT_NUM_ELEMENTS = 1_000_000


def __save_report(initial_report: str, final_report: str, output_dir: str) -> None:
    __save_log(initial_report, "initial", output_dir)
    __save_log(final_report, "final", output_dir)
    __save_experiment_data(initial_report, final_report, output_dir)


def __save_log(report: str, suffix: str, output_dir: str) -> None:
    with open(f"{output_dir}/report_{suffix}.log", "w") as f:
        f.write(report)


def __save_experiment_data(
    initial_report: str, final_report: str, output_dir: str
) -> None:
    initial_memory_usage = kib_to_mib(
        get_current_memory_usage_from_status(initial_report)
    )
    peak_memory_usage = kib_to_mib(get_peak_memory_usage_from_status(final_report))
    final_memory_usage = kib_to_mib(get_current_memory_usage_from_status(final_report))

    with open(f"{output_dir}/results.csv", "w") as f:
        f.write("initial_memory_usage,peak_memory_usage,final_memory_used\n")
        f.write(f"{initial_memory_usage},{peak_memory_usage},{final_memory_usage}")


if __name__ == "__main__":
    output_dir = sys.argv[1]
    num_elements = int(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_NUM_ELEMENTS)

    initial_report = get_self_status()
    consume_large_memory(num_elements)
    final_report = get_self_status()

    __save_report(initial_report, final_report, output_dir)
