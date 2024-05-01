import os
import copy

from uuid import uuid4
from datetime import datetime, timezone
from .context import Context


class SessionContext(Context):
    _initial_data: dict = {
        "pid": os.getpid(),
        "version": "0.1.0",
        "id": None,
        "start_time": None,
        "end_time": None,
        "output_dir": "./",
    }

    @property
    def pid(self) -> int:
        return self.get("pid")

    @property
    def id(self) -> str:
        return self.get("id")

    @property
    def output_dir(self) -> str:
        return self.get("output_dir")

    def __init__(
        self,
        initial_data=None,
    ):
        super().__init__(initial_data=initial_data)
        initial_data = initial_data or self._initial_data

        self.start_session()

    def start_session(self) -> None:
        self.set("start_time", self.__get_current_time())
        self.set("id", self.__generate_id())

    def close_session(self) -> "SessionContext":
        final_profiler_context = copy.deepcopy(self)
        final_profiler_context.set(
            "end_time",
            final_profiler_context.__get_current_time(),
        )

        return final_profiler_context

    def flush(self) -> None:
        self.update(self._initial_data)
        self.start_session()

    def __get_current_time(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def __generate_id(self) -> str:
        return str(uuid4())


session_context = SessionContext()


__all__ = ["session_context", "SessionContext"]
