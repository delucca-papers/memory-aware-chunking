import os

from uuid import uuid4
from dowser.common import Context


class ProfilerContext(Context):
    _base_path: str = "profiler"
    _initial_data: dict = {
        "enabled_types": "memory_usage,time",
        "session": {
            "id": str(uuid4()),
            "pid": os.getpid(),
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


profiler_context = ProfilerContext()


__all__ = ["profiler_context"]
