import os

from resource import struct_rusage
from memory_consuming_task import consume_large_memory
from common.transformers import kib_to_mib
from common.profilers.resource import (
    get_current_memory_usage,
    get_current_memory_usage_from_rusage,
    get_peak_memory_usage_from_rusage,
)

DEFAULT_NUM_ELEMENTS = 1_000_000


def __save_report(
    initial_memory_usage: struct_rusage,
    final_memory_usage: struct_rusage,
    output_dir: str,
) -> None:
    __save_log(initial_memory_usage, "initial", output_dir)
    __save_log(final_memory_usage, "final", output_dir)
    __save_experiment_data(initial_memory_usage, final_memory_usage, output_dir)


def __save_log(memory_usage: struct_rusage, suffix: str, output_dir: str) -> None:
    with open(f"{output_dir}/report_{suffix}.log", "w") as f:
        f.write(str(memory_usage))


def __save_experiment_data(
    initial_memory_usage: struct_rusage,
    final_memory_usage: struct_rusage,
    output_dir: str,
) -> None:
    initial_memory_usage = kib_to_mib(
        get_current_memory_usage_from_rusage(initial_memory_usage)
    )
    peak_memory_usage = kib_to_mib(
        get_peak_memory_usage_from_rusage(final_memory_usage)
    )
    final_memory_usage = kib_to_mib(
        get_current_memory_usage_from_rusage(final_memory_usage)
    )

    with open(f"{output_dir}/results.csv", "w") as f:
        f.write("initial_memory_usage,peak_memory_usage,final_memory_used\n")
        f.write(f"{initial_memory_usage},{peak_memory_usage},{final_memory_usage}")


if __name__ == "__main__":
    output_dir = os.environ.get("TOOL_OUTPUT_DIR")
    num_elements = int(os.environ.get("NUM_ELEMENTS", DEFAULT_NUM_ELEMENTS))

    initial_memory_usage = get_current_memory_usage()
    consume_large_memory(num_elements)
    final_memory_usage = get_current_memory_usage()

    __save_report(initial_memory_usage, final_memory_usage, output_dir)
