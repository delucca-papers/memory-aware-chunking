import json
import os
import copy

from io import TextIOWrapper
from logging import Logger
from toolz import identity
from dowser.logger import get_logger
from dowser.common import normalize_keys_case, Report, session_context, SessionContext
from .context import profiler_context, ProfilerContext
from .types import ProfilerMetric, Profile, Log, Entries, Metadata
from .metrics import to_memory_usage_profile, to_time_profile


class ProfilerReport(Report):
    __logs: list = []
    __profiles: list
    __profiler_context: ProfilerContext
    __session_context: SessionContext
    __logger: Logger

    @classmethod
    def from_filepath(cls, filepath: str) -> "ProfilerReport":
        file = json.load(open(filepath, "r"))
        report_session_context = copy.deepcopy(session_context)
        report_profiler_context = copy.deepcopy(profiler_context)

        report_session_context.update(file.get("session", {}))
        report_profiler_context.update(file.get("context", {}))
        profiles = file.get("profiles", [])

        return cls(report_session_context, report_profiler_context, profiles)

    @property
    def write_stream(self) -> TextIOWrapper:
        output_dir = self.output_dir
        format = self.__profiler_context.report_format
        filename = f"{self.__profiler_context.report_filename}.{format}"
        filepath = os.path.join(output_dir, filename)

        return open(filepath, "w")

    @property
    def output_dir(self) -> str:
        relative_output_dir = self.__profiler_context.report_output_dir
        session_folder = self.__session_context.output_dir

        return os.path.join(session_folder, relative_output_dir)

    def __init__(
        self,
        session_context: SessionContext = session_context,
        profiler_context: ProfilerContext = profiler_context,
        profiles: list = [],
    ):
        self.__logger = get_logger()
        self.__session_context = normalize_keys_case(session_context)
        self.__profiler_context = normalize_keys_case(profiler_context)
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
        self.__session_context = session_context.close_session()
        if len(self.__logs) > 0:
            self.__parse_logs()

        os.makedirs(self.output_dir, exist_ok=True)
        report = self.__to_dict()

        available_formats = {
            "json": self.__save_as_json,
        }

        enabled_format = self.__profiler_context.report_format
        format_handler = available_formats.get(enabled_format)
        if not format_handler:
            raise ValueError(f'Format "{enabled_format} not available')

        return format_handler(report)

    def get_profiles_by_metric(self, metric: str) -> Profile:
        return list(filter(lambda x: x.get("metric") == metric, self.__profiles))

    def __save_as_json(self, report: dict) -> None:
        json.dump(
            normalize_keys_case(report, to_case="camel"),
            self.write_stream,
            indent=4,
        )

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
        output_unit = self.__profiler_context.memory_usage_unit
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
        return {
            "session": self.__session_context.as_dict(),
            "context": self.__profiler_context.as_dict(),
            "profiles": self.__profiles,
        }


__all__ = ["ProfilerReport"]
