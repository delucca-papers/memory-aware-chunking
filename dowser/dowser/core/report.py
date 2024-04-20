import time
import os

from .types import Report, ReportHeaderList, ReportLine
from .config import config
from .file_handling import add_ext, join_path
from .transformers import align_tuples
from .logging import get_logger

get_execution_id = config.lazy_get("execution_id")
get_output_dir = config.lazy_get("output_dir")
get_input_metadata = config.lazy_get("input.metadata")
get_prepend_timestamp = lambda: config.get("report.prepend_timestamp").lower() == "true"


###


def build_headers() -> ReportHeaderList:
    execution_id = get_execution_id()
    input_metadata = get_input_metadata()

    return [("Execution ID", execution_id), ("Input Metadata", input_metadata)]


def build_header_text(header: ReportHeaderList) -> str:
    aligned_headers = align_tuples(header)

    return "\n".join([f"{first}: {second}" for first, second in aligned_headers])


def build_data_text(data: list[ReportLine]) -> str:
    return "\n".join(["\t".join([first, second]) for first, second in data])


def get_execution_output_dir() -> str:
    output_dir = get_output_dir()
    execution_id = get_execution_id()

    return join_path(execution_id, output_dir)


###


def build_report(custom_headers: ReportHeaderList, data: ReportLine) -> Report:
    logger = get_logger()
    logger.info(f"Building report for {len(data)} data points")

    headers = build_headers()
    headers.extend(custom_headers)

    return {
        "headers": headers,
        "data": data,
    }


def save_report(report: Report, relative_path: str) -> None:
    logger = get_logger()
    should_prepend_timestamp = get_prepend_timestamp()
    execution_output_dir = get_execution_output_dir()

    if should_prepend_timestamp:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        relative_path = f"{relative_path}-{timestamp}"

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
