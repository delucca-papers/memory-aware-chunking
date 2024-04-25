import json
import os

from io import TextIOWrapper
from typing import Literal
from toolz import identity, first, compose, second, curry
from toolz.curried import map
from dowser.logger import get_logger
from dowser.common.transformers import convert_keys_to_camel_case, convert_to
from .context import profiler_context

ProfilerType = Literal["time", "memory_usage"]


class ProfilerReport:
    __report_filename = "profiler_report.json"
    __context = profiler_context
    __logger = get_logger()
    __profiles: list[dict] = []

    @property
    def write_stream(self) -> TextIOWrapper:
        filepath = os.path.join(
            self.__context.report_output_dir, self.__report_filename
        )
        return open(filepath, "w")

    @property
    def session(self) -> dict:
        return self.__context.session

    @property
    def profiles(self) -> list[dict]:
        parsers = {
            "time": self.__parse_time_profile,
            "memory_usage": self.__parse_memory_usage_profile,
        }

        return [
            parsers.get(profile.get("type"), identity)(profile)
            for profile in self.__profiles
        ]

    def add_profile(self, type: ProfilerType, data: list, metadata: dict = {}) -> None:
        self.__logger.debug(f"Adding {type} profile to report")
        profile = {
            "type": type,
            "metadata": metadata,
            "data": data,
        }

        self.__profiles.append(profile)

    def save(self) -> None:
        self.__logger.info("Saving profiler report")
        self.__context = profiler_context.close_session()

        json.dump(
            convert_keys_to_camel_case(self.to_dict()), self.write_stream, indent=4
        )

    def to_dict(self) -> dict:
        return {"session": self.session, "profiles": self.profiles}

    def __parse_time_profile(self, profile: dict) -> dict:
        get_record_data = compose(
            lambda r: compose(second, first)(r) if len(r) > 0 else None,
            self.__filter_record_by_key,
        )

        profile_data = profile.get("data", [])

        start_time = get_record_data(profile_data, "START")
        end_time = get_record_data(profile_data, "START")
        total_execution_time = get_record_data(profile_data, "EXECUTION_TIME")

        return {
            "type": "time",
            "metadata": profile.get("metadata"),
            "data": {
                "start": start_time,
                "end": end_time,
                "execution_time": total_execution_time,
            },
        }

    def __parse_memory_usage_profile(self, profile: dict) -> dict:
        profile_data = profile.get("data", [])
        output_unit = self.__context.memory_usage_unit
        parse_data = compose(list, map(self.__parse_memory_usage_record(output_unit)))

        parsed_profile_data = parse_data(profile_data)

        return {
            "type": "memory_usage",
            "metadata": {
                **profile.get("metadata"),
                "unit": output_unit,
                "collected_data_points": len(parsed_profile_data),
            },
            "data": parsed_profile_data,
        }

    @curry
    def __parse_memory_usage_record(
        self,
        output_unit: str,
        record: tuple[int, float, str],
    ) -> dict:
        timestamp, memory_usage, unit = record
        return {
            "timestamp": timestamp,
            "memory_usage": convert_to(output_unit, unit, memory_usage),
        }

    def __filter_record_by_key(self, records: list, key: str) -> list:
        return list(filter(lambda r: r[0] == key, records))


__all__ = ["ProfilerReport"]
