import os

from uuid import uuid4
from datetime import datetime, timezone
from dowser.common import Context


class ProfilerContext(Context):
    _base_path: str = "profiler"
    _initial_data: dict = {
        "enabled_types": "memory_usage,time",
        "session": {
            "id": str(uuid4()),
            "pid": os.getpid(),
            "version": "0.1.0",
            "start_time": None,
            "end_time": None,
            "metadata": {
                "input": "",
            },
        },
        "report": {
            "prefix": "",
            "suffix": "",
            "output_dir": "./",
        },
        "types": {
            "memory_usage": {
                "enabled_backends": "psutil,resource,tracemalloc,mprof,kernel",
                "precision": "4",
                "unit": "mb",
            },
        },
    }

    @property
    def enabled_profilers(self) -> list[str]:
        return self.get("enabled_types").split(",")

    @property
    def memory_usage_enabled_backends(self) -> list[str]:
        return self.get("types.memory_usage.enabled_backends").split(",")

    @property
    def memory_usage_precision(self) -> float:
        return 10 ** -int(self.get("types.memory_usage.precision"))

    @property
    def session_pid(self) -> int:
        return self.get("session.pid")

    def __init__(
        self,
        initial_data: dict | None = None,
    ):
        super().__init__(initial_data=initial_data)
        initial_data = initial_data or self._initial_data

        self.start_session()

    def start_session(self) -> None:
        self.set("session.start_time", self.__get_current_time())

    def __get_current_time(self) -> str:
        return datetime.now(timezone.utc).isoformat()


profiler_context = ProfilerContext()


__all__ = ["profiler_context"]
