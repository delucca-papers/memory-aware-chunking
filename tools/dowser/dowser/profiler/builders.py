import pyarrow as pa
import pyarrow.parquet as pq

from collections import defaultdict
from typing import List, Tuple, Any, Dict, Optional
from dowser.config import MemoryUsageBackend, ProfilerMetric, FunctionParameter
from dowser.common.transformers import deep_merge
from dowser.common.logger import logger
from .memory_usage import build_trace_hooks as build_memory_usage_trace_hooks
from .time import build_trace_hooks as build_time_trace_hooks
from .types import TraceHooks, TraceList


__all__ = ["build_trace_hooks", "build_profile", "build_metadata"]

def build_trace_hooks(
    enabled_metrics: List[ProfilerMetric],
    enabled_memory_usage_backends: List[MemoryUsageBackend],
) -> TraceHooks:
    memory_usage_hooks = (
        build_memory_usage_trace_hooks(enabled_memory_usage_backends)
        if ProfilerMetric.MEMORY_USAGE in enabled_metrics
        else {}
    )
    time_hooks = (
        build_time_trace_hooks() if ProfilerMetric.TIME in enabled_metrics else {}
    )
    return deep_merge(memory_usage_hooks, time_hooks, append=True)


def build_profile(
    trace_list: TraceList,
    output_dir: str,
    file_name: str,
    metadata: Dict,
) -> str:
    logger.info("Building output profile file")
    logger.debug(f"Using {len(trace_list)} traces")

    schema = build_profile_parquet_schema()
    logger.debug(f"Using schema:\n{schema}")

    table = build_profile_table(trace_list, schema)
    table = apply_metadata(metadata, table)
    logger.debug(f"Using table metadata: {table.schema.metadata}")

    file_path = f"{output_dir}/{file_name}.parquet"
    pq.write_table(table, file_path)
    logger.info(f"Profile file saved at: {file_path}")

    return file_path


def build_metadata(
    signature: List[FunctionParameter], args: Tuple, kwargs: Dict
) -> Dict:
    entrypoint_args_names = [param.name for param in signature]
    entrypoint_args = {entrypoint_args_names[i]: str(arg) for i, arg in enumerate(args)}
    entrypoint_kwargs = {k: str(v) for k, v in kwargs.items()}

    return {
        **{
            f"entrypoint_{arg_name}": arg_value
            for arg_name, arg_value in entrypoint_args.items()
        },
        **{
            f"entrypoint_{arg_name}": arg_value
            for arg_name, arg_value in entrypoint_kwargs.items()
        },
        "kernel_memory_usage_unit": "kb",
        "psutil_memory_usage_unit": "b",
        "resource_memory_usage_unit": "kb",
        "tracemalloc_memory_usage_unit": "b",
        "unix_timestamp_unit": "ms",
    }


def build_profile_parquet_schema() -> pa.Schema:
    return pa.schema(
        [
            ("source", pa.string()),
            ("function", pa.string()),
            ("event", pa.string()),
            ("kernel_memory_usage", pa.float32()),
            ("psutil_memory_usage", pa.float32()),
            ("resource_memory_usage", pa.float32()),
            ("tracemalloc_memory_usage", pa.float32()),
            ("unix_timestamp", pa.int64()),
        ]
    )


def build_profile_table(trace_list: TraceList, schema: pa.schema) -> pa.table:
    columns = defaultdict(list, {field.name: [] for field in schema})
    for trace in trace_list:
        for key in schema.names:
            columns[key].append(trace.get(key))

    return pa.Table.from_arrays(
        [
            columns["source"],
            columns["function"],
            columns["event"],
            columns["kernel_memory_usage"],
            columns["psutil_memory_usage"],
            columns["resource_memory_usage"],
            columns["tracemalloc_memory_usage"],
            columns["unix_timestamp"],
        ],
        schema=schema,
    )


def apply_metadata(metadata: Dict, table: pa.Table) -> pa.Table:
    updated_metadata = table.schema.metadata or {}
    updated_metadata.update(
        {k.encode("utf-8"): v.encode("utf-8") for k, v in metadata.items()}
    )
    return table.replace_schema_metadata(updated_metadata)
