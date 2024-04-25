import os
import copy

from uuid import uuid4
from datetime import datetime, timezone
from dowser.common import Context
from dowser.logger import get_logger


class ProfilerContext(Context):
    _base_path: str = "profiler"
    _initial_data: dict = {
        "enabled_types": "memory_usage,time",
        "session": {
            "pid": os.getpid(),
            "version": "0.1.0",
            "id": None,
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
    __logger = get_logger()

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

    @property
    def report_output_dir(self) -> str:
        return self.get("report.output_dir")

    @property
    def session(self) -> dict:
        return self.get("session")

    def __init__(
        self,
        initial_data: dict | None = None,
    ):
        super().__init__(initial_data=initial_data)
        initial_data = initial_data or self._initial_data

        self.start_session()

    def start_session(self) -> None:
        self.__logger.info("Starting new profiler session")

        self.set("session.start_time", self.__get_current_time())
        self.set("session.id", self.__generate_id())

    def close_session(self) -> "ProfilerContext":
        self.__logger.info("Closing profiler session")

        self.set("session.end_time", self.__get_current_time())
        final_profiler_context = copy.deepcopy(self)
        self.flush()

        return final_profiler_context

    def flush(self) -> None:
        self.__logger.debug("Flushing profiler context")
        self.update(self._initial_data)
        self.start_session()

    def __get_current_time(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def __generate_id(self) -> str:
        return str(uuid4())


profiler_context = ProfilerContext()


__all__ = ["profiler_context"]
