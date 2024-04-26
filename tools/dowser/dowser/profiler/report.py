import json
import os
import copy

from io import TextIOWrapper
from logging import Logger
from toolz import identity
from dowser.logger import get_logger
from dowser.common import normalize_keys_case, Report
from .context import profiler_context, ProfilerContext
from .types import ProfilerMetric, Profile, Log, Entries, Metadata
from .metrics import to_memory_usage_profile, to_time_profile


class ProfilerReport(Report):
    __report_filename = "profiler-report.json"
    __logs: list[Log] = []
    __profiles: list[Profile]
    __context: ProfilerContext
    __logger: Logger

    @classmethod
    def from_filepath(cls, filepath: str) -> "ProfilerReport":
        file = json.load(open(filepath, "r"))
        context = copy.deepcopy(profiler_context)
        context.update({"session": file.get("session", {})})
        profiles = file.get("profiles", [])

        return cls(context, profiles)

    @property
    def write_stream(self) -> TextIOWrapper:
        filepath = os.path.join(
            self.__context.report_output_dir, self.__report_filename
        )
        return open(filepath, "w")

    @property
    def output_dir(self) -> str:
        return self.__context.report_output_dir

    def __init__(
        self,
        context: ProfilerContext = profiler_context,
        profiles: list[dict] = [],
    ):
        self.__logger = get_logger()
        self.__context = normalize_keys_case(context)
        self.__profiles = normalize_keys_case(profiles)

    def add_log(
        self,
        metric: ProfilerMetric,
        entries: Log,
        metadata: dict = {},
    ) -> None:
        self.__logger.debug(f"Adding {metric} log entries to report")
        metadata = {
            **metadata,
            "collected_entries": len(entries),
        }

        self.__logs.append((metric, entries, metadata))

    def save(self) -> None:
        self.__logger.info("Saving profiler report")
        self.__context = profiler_context.close_session()
        if len(self.__logs) > 0:
            self.__parse_logs()

        os.makedirs(self.output_dir, exist_ok=True)
        report = self.__to_dict()

        json.dump(
            normalize_keys_case(report, to_case="camel"),
            self.write_stream,
            indent=4,
        )

    def get_profiles_by_metric(self, metric: str) -> Profile:
        return list(filter(lambda x: x.get("metric") == metric, self.__profiles))

    def __parse_logs(self) -> None:
        available_parsers = {
            "time": self.__parse_time_log,
            "memory_usage": self.__parse_memory_usage_log,
        }

        self.__profiles = [
            available_parsers.get(metric, identity)(entries, metadata)
            for metric, entries, metadata in self.__logs
        ]
        self.__logs = []

    def __parse_memory_usage_log(self, entries: Entries, metadata: Metadata) -> Profile:
        output_unit = self.__context.memory_usage_unit
        log_unit = metadata.get("unit")

        return {
            "metric": "memory_usage",
            "metadata": {
                **metadata,
                "unit": output_unit,
            },
            "entries": to_memory_usage_profile(output_unit, log_unit, entries),
        }

    def __parse_time_log(self, entries: Entries, metadata: Metadata) -> Profile:
        return {
            "metric": "time",
            "metadata": metadata,
            "entries": to_time_profile(entries),
        }

    def __to_dict(self) -> dict:
        return {"session": self.__context.session, "profiles": self.__profiles}


__all__ = ["ProfilerReport"]
