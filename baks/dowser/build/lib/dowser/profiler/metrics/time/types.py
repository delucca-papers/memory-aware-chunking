from typing import Literal, TypedDict

EventType = Literal["START", "END", "EXECUTION_TIME"]
Time = float

TimeRecord = tuple[EventType, Time]
TimeLog = list[TimeRecord]


class TimeEntry(TypedDict):
    event_type: EventType
    time: Time


TimeProfile = list[TimeEntry]


__all__ = ["TimeLog", "TimeRecord", "TimeProfile", "TimeProfile", "TimeEntry"]
