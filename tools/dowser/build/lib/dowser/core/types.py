from typing import Callable, TypedDict

ThreadWrappedResult = tuple[list, ...]
ThreadWrapper = Callable[..., ThreadWrappedResult]

ReportHeader = tuple[str, str]
ReportHeaderList = tuple[ReportHeader]
ReportColumn = tuple[str, str]
ReportLine = tuple[ReportColumn]


class Report(TypedDict):
    headers: ReportHeaderList
    data: list[ReportLine]


__all__ = [
    "ThreadWrapper",
    "ThreadWrappedResult",
    "ReportHeaderList",
    "Report",
    "ReportLine",
]
