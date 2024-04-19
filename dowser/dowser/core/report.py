import time
import os

from .types import Report, ReportHeaderList, ReportLine
from .config import config, get_config
from .file_handling import add_prefix_to_file_in_path, add_ext, join_path
from .transformers import align_tuples
from .logging import get_logger

get_execution_id = lambda c: get_config("execution_id", c)
get_input_metadata = lambda c: get_config("input.metadata", c)
get_prepend_timestamp = (
    lambda c: get_config("report.prepend_timestamp", c).lower() == "true"
)
get_output_dir = lambda c: get_config("output_dir", c)


###


def build_headers(config: dict = config) -> ReportHeaderList:
    execution_id = get_execution_id(config)
    input_metadata = get_input_metadata(config)

    return [("Execution ID", execution_id), ("Input Metadata", input_metadata)]


def build_header_text(header: ReportHeaderList) -> str:
    aligned_headers = align_tuples(header)

    return "\n".join([f"{first}: {second}" for first, second in aligned_headers])


def build_data_text(data: list[ReportLine]) -> str:
    return "\n".join(["\t".join([first, second]) for first, second in data])


def get_execution_output_dir(config: dict = config) -> str:
    output_dir = get_output_dir(config)
    execution_id = get_execution_id(config)

    return join_path(execution_id, output_dir)


###


def build_report(
    custom_headers: ReportHeaderList,
    data: ReportLine,
    config: dict = config,
) -> Report:
    logger = get_logger(config)
    logger.info(f"Building report for {len(data)} data points")

    headers = build_headers(config)
    headers.extend(custom_headers)

    return {
        "headers": headers,
        "data": data,
    }


def save_report(
    report: Report,
    relative_path: str,
    config: dict = config,
) -> None:
    logger = get_logger(config)
    should_prepend_timestamp = get_prepend_timestamp(config)
    execution_output_dir = get_execution_output_dir(config)

    if should_prepend_timestamp:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        relative_path = add_prefix_to_file_in_path(timestamp, relative_path)

    relative_path = add_ext("dat", relative_path)
    absolute_path = join_path(relative_path, execution_output_dir)

    logger.info(f"Saving report to {absolute_path}")

    header_text = build_header_text(report["headers"])
    data_text = build_data_text(report["data"])

    os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
    with open(absolute_path, "w") as f:
        f.write(header_text)
        f.write("\n\n")
        f.write(data_text)

    logger.info(f"Report saved to {absolute_path}")


__all__ = ["build_report", "save_report"]
