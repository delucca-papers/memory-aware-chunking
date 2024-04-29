from typing import Literal, TypedDict

EventType = Literal["CALL", "RETURN"]
Function = str
Time = float

TimeRecord = tuple[Time, EventType, Function]
TimeLog = list[TimeRecord]


class TimeEntry(TypedDict):
    event_type: EventType
    time: Time


TimeProfile = list[TimeEntry]


__all__ = ["TimeLog", "TimeRecord", "TimeProfile", "TimeProfile", "TimeEntry"]
