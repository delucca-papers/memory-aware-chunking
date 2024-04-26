from typing import Literal, TypedDict

Entries = list
Metadata = dict
ProfilerMetric = Literal["time", "memory_usage"]
Log = tuple[ProfilerMetric, Entries, Metadata]


class Profile(TypedDict):
    metric: ProfilerMetric
    metadata: dict
    entries: list


__all__ = ["ProfilerMetric", "ProfileEntry", "Log", "Entries", "Metadata"]
