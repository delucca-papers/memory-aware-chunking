from dowser.common import Context


class ProfilerContext(Context):
    _base_path: str = "profiler"
    _initial_data: dict = {
        "enabled_metrics": "memory_usage,time",
        "report": {
            "filename": "profiles",
            "format": "json",
            "output_dir": "./",
        },
        "metrics": {
            "memory_usage": {
                "enabled_backends": "psutil,resource,tracemalloc,mprof,kernel",
                "precision": "4",
                "unit": "mb",
            },
        },
    }

    @property
    def enabled_profilers(self) -> list[str]:
        return self.get("enabled_metrics").split(",")

    @property
    def memory_usage_enabled_backends(self) -> list[str]:
        return self.get("metrics.memory_usage.enabled_backends").split(",")

    @property
    def memory_usage_precision(self) -> float:
        return 10 ** -int(self.get("metrics.memory_usage.precision"))

    @property
    def memory_usage_unit(self) -> str:
        return self.get("metrics.memory_usage.unit")

    @property
    def report_output_dir(self) -> str:
        return self.get("report.output_dir")

    @property
    def report_filename(self) -> str:
        return self.get("report.filename")

    @property
    def report_format(self) -> str:
        return self.get("report.format")


profiler_context = ProfilerContext()


__all__ = ["profiler_context", "ProfilerContext"]
