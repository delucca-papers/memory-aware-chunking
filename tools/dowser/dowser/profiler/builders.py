import pyarrow as pa
import pyarrow.parquet as pq

from typing import List, Tuple, List, Any
from dowser.config import MemoryUsageBackend, ProfilerMetric, FunctionParameter
from dowser.common.transformers import deep_merge
from dowser.common.logger import logger
from .memory_usage import build_trace_hooks as build_memory_usage_trace_hooks
from .time import build_trace_hooks as build_time_trace_hooks
from .types import TraceHooks, TraceList


__all__ = ["build_trace_hooks", "build_profile", "build_metadata"]


def build_metadata(
    signature: List[FunctionParameter],
    args: tuple,
    kwargs: dict,
) -> dict:
    args_names = [param.name for param in signature]
    args_metadata = {args_names[i]: str(arg) for i, arg in enumerate(args)}
    kwargs_metadata = {k: str(v) for k, v in kwargs.items()}

    return {**args_metadata, **kwargs_metadata}


def build_trace_hooks(
    enabled_metrics: List[ProfilerMetric],
    enabled_memory_usage_backends: List[MemoryUsageBackend],
) -> TraceHooks:
    memory_usage_trace_hooks = (
        build_memory_usage_trace_hooks(enabled_memory_usage_backends)
        if ProfilerMetric.MEMORY_USAGE in enabled_metrics
        else {}
    )
    time_trace_hooks = (
        build_time_trace_hooks() if ProfilerMetric.TIME in enabled_metrics else {}
    )

    return deep_merge(memory_usage_trace_hooks, time_trace_hooks, append=True)


def build_profile(
    trace_list: TraceList,
    output_dir: str,
    file_name: str,
    metadata: dict,
) -> str:
    logger.info("Building output profile file")

    file_path = f"{output_dir}/{file_name}.parquet"
    schema = build_profile_parquet_schema()
    logger.debug(f"Using schema:\n{schema}")

    (
        timestamps,
        source_locations,
        function_names,
        event_types,
        additional_data,
    ) = build_profile_parquet_data(trace_list)
    logger.debug(f"Using data: {len(timestamps)} records")

    table = pa.Table.from_arrays(
        [
            timestamps,
            source_locations,
            function_names,
            event_types,
            additional_data,
        ],
        schema=schema,
    )

    updated_metadata = table.schema.metadata or {}
    updated_metadata.update(
        {k.encode("utf-8"): v.encode("utf-8") for k, v in metadata.items()}
    )
    table = table.replace_schema_metadata(updated_metadata)

    pq.write_table(
        table,
        file_path,
    )

    logger.info(f"Profile file saved at: {file_path}")

    return file_path


def build_profile_parquet_schema() -> pa.Schema:
    return pa.schema(
        [
            ("timestamp", pa.string()),
            ("source", pa.string()),
            ("function_name", pa.string()),
            ("event_type", pa.string()),
            ("additional_data", pa.list_(pa.list_(pa.string()))),
        ]
    )


def build_profile_parquet_data(trace_list: TraceList) -> Tuple[
    List[str],
    List[str],
    List[str],
    List[str],
    List[List[List[str]]],
]:
    timestamps = []
    source_locations = []
    function_names = []
    event_types = []
    additional_data = []

    for trace in trace_list:
        timestamps.append(str(trace[0]))
        source_locations.append(trace[1])
        function_names.append(trace[2])
        event_types.append(trace[3])
        additional_data.append(build_additional_data(trace[4:][0]))

    return (
        timestamps,
        source_locations,
        function_names,
        event_types,
        additional_data,
    )


def build_additional_data(data: List[List[Any]]) -> List[List[str]]:
    return [[str(item) for item in sublist] for sublist in data]
