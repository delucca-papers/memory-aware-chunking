import sys

from typing import NamedTuple
from memory_consuming_task import consume_large_memory
from common.transformers import bytes_to_mib
from common.profilers.psutil import (
    get_self_memory_info,
    get_current_memory_usage_from_pmem,
    get_peak_memory_usage_from_pmem,
)

DEFAULT_NUM_ELEMENTS = 1_000_000


def __save_report(
    initial_memory_usage: NamedTuple, final_memory_usage: NamedTuple, output_dir: str
) -> None:
    __save_log(initial_memory_usage, "initial", output_dir)
    __save_log(final_memory_usage, "final", output_dir)
    __save_experiment_data(initial_memory_usage, final_memory_usage, output_dir)


def __save_log(memory_usage: NamedTuple, suffix: str, output_dir: str) -> None:
    with open(f"{output_dir}/report_{suffix}.log", "w") as f:
        f.write(str(memory_usage))


def __save_experiment_data(
    initial_memory_usage: NamedTuple, final_memory_usage: NamedTuple, output_dir: str
) -> None:
    initial_memory_usage = bytes_to_mib(
        get_current_memory_usage_from_pmem(initial_memory_usage)
    )
    peak_memory_usage = bytes_to_mib(
        get_peak_memory_usage_from_pmem(final_memory_usage)
    )
    final_memory_usage = bytes_to_mib(
        get_current_memory_usage_from_pmem(final_memory_usage)
    )

    with open(f"{output_dir}/results.csv", "w") as f:
        f.write("initial_memory_usage,peak_memory_usage,final_memory_used\n")
        f.write(f"{initial_memory_usage},{peak_memory_usage},{final_memory_usage}")


if __name__ == "__main__":
    output_dir = sys.argv[1]
    num_elements = int(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_NUM_ELEMENTS)

    initial_memory_usage = get_self_memory_info()
    consume_large_memory(num_elements)
    final_memory_usage = get_self_memory_info()

    __save_report(initial_memory_usage, final_memory_usage, output_dir)
