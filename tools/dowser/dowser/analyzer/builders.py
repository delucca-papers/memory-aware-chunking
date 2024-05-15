import pandas as pd

from dowser.common.logger import logger
from dowser.config import MemoryUsageUnit
from .trace import Trace


__all__ = ["build_trace_tree", "build_metadata_annotation"]


def build_metadata_annotation(df: pd.DataFrame) -> str:
    entrypoint_metadata = [
        (key.replace("entrypoint_", ""), value)
        for key, value in df.attrs.items()
        if key.startswith("entrypoint_")
    ]
    metadata_str = ", ".join(f"{key}={value}" for key, value in entrypoint_metadata)

    return metadata_str


def build_trace_tree(df: pd.DataFrame) -> Trace:
    logger.info(f"Building trace tree for {len(df)} events")

    root = build_root_trace(df)
    current_trace = root
    stack = [root]

    for _, row in df.iterrows():
        trace = Trace.from_pandas_row(row)

        if trace.event_type == "call":
            current_trace.add_child(trace)
            stack.append(trace)
            current_trace = trace
        elif trace.event_type == "return":
            if len(stack) > 1:
                stack.pop()
                current_trace = stack[-1]

    return root


def build_root_trace(df: pd.DataFrame) -> Trace:
    return Trace(
        df.iloc[0]["timestamp"],
        "root",
        "root",
        "root",
    )
