from pydantic import BaseModel, field_validator

from enum import Enum


__all__ = (["LoggerConfig", "Transport"],)


class Transport(Enum):
    CONSOLE = "CONSOLE"
    FILE = "FILE"


class Level(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggerConfig(BaseModel):
    enabled_transports: list[Transport] = [Transport.CONSOLE, Transport.FILE]
    level: Level = Level.INFO

    @field_validator("enabled_transports", mode="before")
    def uppercase_enabled_transports(cls, v: any) -> list[Transport]:
        if isinstance(v, list):
            return [Transport(i.upper()) for i in v]

        return v

    @field_validator("level", mode="before")
    def uppercase_level(cls, v: any) -> Level:
        if isinstance(v, str):
            v = v.upper()

        return Level(v)
