import pyarrow as pa
import pyarrow.parquet as pq

from collections import defaultdict
from typing import Dict
from toolz import curry
from .types import TraceList


__all__ = ["save_profile"]


@curry
def save_profile(
    output_dir: str,
    file_name: str,
    metadata: Dict,
    trace_list: TraceList,
) -> None:
    schema = build_profile_parquet_schema()
    file_path = f"{output_dir}/{file_name}.parquet"

    table = build_profile_table(trace_list, schema)
    table = apply_metadata(metadata, table)
    table = merge_with_existing_profile(file_path, table)

    pq.write_table(table, file_path)


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
    default_value = {
        "source": "UNKNOWN",
        "function": "UNKNOWN",
        "event": "UNKNOWN",
        "kernel_memory_usage": 0,
        "psutil_memory_usage": 0,
        "resource_memory_usage": 0,
        "tracemalloc_memory_usage": 0,
        "unix_timestamp": 0,
    }

    columns = defaultdict(list, {field.name: [] for field in schema})
    for trace in trace_list:
        for key in schema.names:
            columns[key].append(trace.get(key, default_value[key]))

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


def merge_with_existing_profile(file_path: str, table: pa.Table) -> pa.Table:
    try:
        existing_table = pq.read_table(file_path)
        return pa.concat_tables([existing_table, table])
    except FileNotFoundError:
        return table
