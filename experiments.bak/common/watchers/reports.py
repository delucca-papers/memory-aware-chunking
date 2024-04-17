import os

from ..transformers import dataset_path_to_name
from ..events import EventName
from .memory_usage import save_memory_usage_report
from .execution_time import save_execution_time_report
from .constants import MEMORY_USAGE_RESULTS_NAME


def get_peak_memory_used(watcher_results: dict) -> int:
    memory_usages = [
        memory_used for _, memory_used in watcher_results[MEMORY_USAGE_RESULTS_NAME]
    ]

    return max(memory_usages)


def save_reports(
    watcher_results: dict,
    dataset_path: str,
    attribute_name: str,
    output_dir: str,
    iteration_num: int,
) -> None:
    dataset_name = dataset_path_to_name(dataset_path)
    reports_dir = os.path.join(output_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    save_memory_usage_report(
        watcher_results,
        attribute_name,
        iteration_num,
        dataset_name,
        reports_dir,
    )

    save_execution_time_report(
        watcher_results,
        attribute_name,
        iteration_num,
        dataset_name,
        reports_dir,
    )
