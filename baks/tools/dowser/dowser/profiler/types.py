from typing import Literal, TypedDict

Entries = list
ProfilerMetric = Literal["time", "memory_usage"]


class Profile(TypedDict):
    metric: ProfilerMetric
    metadata: dict
    entries: list


class Metadata(TypedDict):
    inputs: str
    function_path: str
    collected_entries: int


Log = tuple


__all__ = ["ProfilerMetric", "ProfileEntry", "Log", "Entries", "Metadata"]
