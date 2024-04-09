import io
import os

from memory_consuming_task import consume_large_memory
from common.profilers.mprof import (
    run_profiled,
    get_initial_memory_usage_from_report,
    get_peak_memory_usage_from_report,
    get_final_memory_usage_from_report,
)

DEFAULT_NUM_ELEMENTS = 1_000_000


def __save_report(report: io.StringIO, output_dir: str) -> None:
    __save_log(report, output_dir)
    __save_experiment_data(report, output_dir)


def __save_log(report: io.StringIO, output_dir: str) -> None:
    with open(f"{output_dir}/report.log", "w") as f:
        f.write(report.getvalue())


def __save_experiment_data(report: io.StringIO, output_dir: str) -> None:
    initial_memory_usage_report = get_initial_memory_usage_from_report(report)
    peak_memory_usage_report = get_peak_memory_usage_from_report(report)
    final_memory_usage_report = get_final_memory_usage_from_report(report)

    initial_memory_usage = initial_memory_usage_report["value"]
    peak_memory_usage = peak_memory_usage_report["value"]
    final_memory_usage = final_memory_usage_report["value"]

    with open(f"{output_dir}/results.csv", "w") as f:
        f.write("initial_memory_usage,peak_memory_usage,final_memory_used\n")
        f.write(f"{initial_memory_usage},{peak_memory_usage},{final_memory_usage}")


if __name__ == "__main__":
    output_dir = os.environ.get("TOOL_OUTPUT_DIR")
    num_elements = int(os.environ.get("NUM_ELEMENTS", DEFAULT_NUM_ELEMENTS))

    report = run_profiled(consume_large_memory, num_elements)
    __save_report(report, output_dir)
