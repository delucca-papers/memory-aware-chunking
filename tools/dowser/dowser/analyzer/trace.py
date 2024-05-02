import pandas as pd

from typing import List
from .types import CollectedTraceList
from dowser.config import ProfilerMetric


__all__ = ["Trace"]


class Trace:
    timestamp: float
    source: str
    function_name: str
    event_type: str
    collected_traces: CollectedTraceList
    children: List["Trace"]

    @classmethod
    def from_pandas_row(cls, row: pd.Series) -> "Trace":
        return cls(
            row["timestamp"],
            row["source"],
            row["function_name"],
            row["event_type"],
            row["additional_data"],
        )

    def __init__(
        self,
        timestamp: float,
        source: str,
        function_name: str,
        event_type: str,
        collected_traces: CollectedTraceList = [],
    ):
        self.timestamp = timestamp
        self.source = source
        self.function_name = function_name
        self.event_type = event_type
        self.collected_traces = collected_traces
        self.children = []

    def add_child(self, child: "Trace") -> None:
        self.children.append(child)
