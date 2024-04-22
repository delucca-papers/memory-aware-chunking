import time

from toolz import curry, compose
from ..core import get_logger, to_absolute_output_path, add_ext
from ..contexts import report_context, config
from .types import ReportData, ReportMetadata, Report


get_report_group = report_context.lazy_get("group")
get_append_timestamp = lambda: config.get("report.append_timestamp").lower() == "true"


def append_timestamp(path: str) -> str:
    should_append_timestamp = get_append_timestamp()
    if should_append_timestamp:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        path = f"{path}-{timestamp}"

    return path


def add_group(path: str) -> str:
    report_group = get_report_group()
    if report_group:
        path = f"{report_group}/{path}"

    return path


###


build_report_path = compose(
    to_absolute_output_path,
    add_group,
    append_timestamp,
    add_ext("dat"),
)


@curry
def build_report(metadata: ReportMetadata, data: ReportData) -> Report:
    logger = get_logger()
    logger.info(f"Building report for {len(data)} data points")

    return {
        "metadata": metadata,
        "data": data,
    }


__all__ = ["build_report", "build_report_path"]
