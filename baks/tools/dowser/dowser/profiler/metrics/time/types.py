from typing import Literal, TypedDict

EventType = Literal["START", "END", "EXECUTION_TIME"]
Time = float

TimeRecord = tuple
TimeLog = list


class TimeEntry(TypedDict):
    event_type: EventType
    time: Time


TimeProfile = list


__all__ = ["TimeLog", "TimeRecord", "TimeProfile", "TimeProfile", "TimeEntry"]
