from typing import Literal

EventType = Literal["START", "END", "EXECUTION_TIME"]
Timestamp = float

TimeRecord = tuple[EventType, Timestamp]
TimeLog = list[TimeRecord]


__all__ = ["TimeLog", "TimeRecord"]
