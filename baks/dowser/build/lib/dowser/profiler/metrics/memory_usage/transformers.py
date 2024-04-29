from toolz import compose, curry
from toolz.curried import map
from dowser.common import convert_to_unit
from .types import (
    MemoryUsageLog,
    MemoryUnit,
    MemoryUsageRecord,
    MemoryUsageProfile,
    MemoryUsageEntry,
)


def to_memory_usage_profile(
    output_unit: MemoryUnit,
    log_unit: MemoryUnit,
    log: MemoryUsageLog,
) -> MemoryUsageProfile:
    return compose(
        list,
        map(to_memory_usage_profile_entry(output_unit, log_unit)),
    )(log)


@curry
def to_memory_usage_profile_entry(
    output_unit: MemoryUnit,
    log_unit: MemoryUnit,
    record: MemoryUsageRecord,
) -> MemoryUsageEntry:
    timestamp, memory_usage = record

    return {
        "timestamp": timestamp,
        "memory_usage": convert_to_unit(output_unit, log_unit, memory_usage),
    }


__all__ = ["to_memory_usage_profile"]
