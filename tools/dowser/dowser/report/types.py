from typing import TypedDict

ReportRow = tuple[str, str]
ReportMetadata = tuple[ReportRow]
ReportData = tuple[ReportRow]


class Report(TypedDict):
    metadata: ReportMetadata
    data: ReportData


__all__ = ["Report", "ReportData", "ReportMetadata", "ReportRow"]
