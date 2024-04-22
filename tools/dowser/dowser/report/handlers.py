import os

from ..core import get_logger
from .types import ReportMetadata, ReportData
from .builders import build_report_path, build_report
from .metadata.builders import build_extended_metadata, build_metadata_text
from .data.builders import build_data_text


def save_report(
    data: ReportData,
    relative_path: str,
    custom_metadata: ReportMetadata | None = None,
) -> str:
    logger = get_logger()
    absolute_path = build_report_path(relative_path)
    os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

    logger.info(f"Saving report to {absolute_path}")

    metadata = build_extended_metadata(custom_metadata)
    report = build_report(metadata, data)

    metadata_text = build_metadata_text(report["metadata"])
    data_text = build_data_text(report["data"])

    with open(absolute_path, "w") as f:
        f.write(metadata_text)
        f.write("\n\n")
        f.write(data_text)

    logger.info(f"Report saved to {absolute_path}")
