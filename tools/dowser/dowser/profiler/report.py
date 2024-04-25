from typing import Literal
from dowser.logger import get_logger
from .context import profiler_context

ProfilerType = Literal["time", "memory_usage"]


class ProfilerReport:
    __context = profiler_context
    __logger = get_logger()
    __profiles: list[dict] = []

    def add_profile(self, type: ProfilerType, data: list, metadata: dict = {}) -> None:
        self.__logger.debug(f"Adding {type} profile to report")
        profile = {
            "type": type,
            "metadata": metadata,
            "data": data,
        }

        self.__profiles.append(profile)
        # TODO: PAREI AQUI

    def save(self) -> None:
        self.__logger.info("Saving profiler report")
        self.__context = profiler_context.close_session()


__all__ = ["ProfilerReport"]
