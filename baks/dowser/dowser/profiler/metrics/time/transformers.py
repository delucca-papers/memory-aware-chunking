from toolz import compose
from toolz.curried import map
from .types import (
    TimeLog,
    TimeProfile,
    TimeRecord,
    TimeEntry,
)


def to_time_profile(log: TimeLog) -> TimeProfile:
    return compose(
        list,
        map(to_time_profile_entry),
    )(log)


def to_time_profile_entry(record: TimeRecord) -> TimeEntry:
    timestamp, event_type, time = record

    return {"timestamp": timestamp, "event_type": event_type, "time": time}


__all__ = ["to_time_profile"]
