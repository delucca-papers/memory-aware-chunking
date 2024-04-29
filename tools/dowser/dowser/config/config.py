import os
import toml

from pydantic import BaseModel, DirectoryPath, field_validator
from argparse import Namespace
from dowser.common.transformers import filter_defined_values, str_as_list, deep_merge
from .logger import LoggerConfig
from .profiler import ProfilerConfig


__all__ = ["Config"]

initial_config = {
    "output_dir": "./",
    "logger": {
        "enabled_transports": ["CONSOLE", "FILE"],
        "level": "INFO",
    },
    "profiler": {
        "enabled_metrics": ["MEMORY_USAGE", "TIME"],
        "memory_usage": {
            "enabled_backends": ["KERNEL"],
            "unit": "MB",
        },
    },
}


class Config(BaseModel):
    output_dir: DirectoryPath
    logger: LoggerConfig
    profiler: ProfilerConfig

    @field_validator("output_dir")
    def create_dir_if_not_exists(cls, v):
        if not os.path.isdir(v):
            os.makedirs(v, exist_ok=True)
        return v

    @staticmethod
    def parse_env() -> dict:
        return filter_defined_values(
            {
                "session_id": os.environ.get("DOWSER_SESSION_ID"),
                "output_dir": os.environ.get("DOWSER_OUTPUT_DIR"),
                "log_level": os.environ.get("DOWSER_LOG_LEVEL"),
                "log_transport": str_as_list(os.environ.get("DOWSER_LOG_TRANSPORT")),
                "enable_metric": str_as_list(os.environ.get("DOWSER_ENABLE_METRIC")),
                "enable_mem_backend": str_as_list(
                    os.environ.get("DOWSER_ENABLE_MEM_BACKEND")
                ),
                "mem_unit": os.environ.get("DOWSER_MEM_UNIT"),
            },
            allow_empty_lists=False,
        )

    @staticmethod
    def parse_file(
        config_file_path: str = os.environ.get("DOWSER_CONFIG", "dowser.toml"),
    ) -> dict:
        try:
            loaded_config = toml.load(config_file_path)
        except Exception as _:
            return {}

        return filter_defined_values(
            {
                **loaded_config,
                "logger": {
                    **loaded_config.get("logger", {}),
                    "enabled_transports": str_as_list(
                        loaded_config.get("logger", {}).get("enabled_transports"),
                    ),
                },
                "profiler": {
                    **loaded_config.get("profiler", {}),
                    "enabled_metrics": str_as_list(loaded_config.get("enable_metric")),
                    "memory_usage": {
                        **loaded_config.get("profiler", {}).get("memory_usage", {}),
                        "enabled_backends": str_as_list(
                            loaded_config.get("enable_mem_backend")
                        ),
                    },
                },
            },
            allow_empty_lists=False,
        )

    @staticmethod
    def from_flat_config(flag_config: dict) -> dict:
        return filter_defined_values(
            {
                "output_dir": flag_config.get("output_dir"),
                "logger": {
                    "enabled_transports": flag_config.get("log_transport"),
                    "level": flag_config.get("log_level"),
                },
                "profiler": {
                    "session_id": flag_config.get("session_id"),
                    "enabled_metrics": flag_config.get("enable_metric"),
                    "script": flag_config.get("script"),
                    "args": flag_config.get("args"),
                    "memory_usage": {
                        "enabled_backends": flag_config.get("enable_mem_backend"),
                        "unit": flag_config.get("mem_unit"),
                    },
                },
            },
            allow_empty_lists=False,
        )

    @classmethod
    def from_namespace(cls, namespace: Namespace) -> "Config":
        env_config = cls.from_flat_config(cls.parse_env())
        file_config = cls.parse_file()

        namespace_config = cls.from_flat_config(namespace.__dict__)

        config = deep_merge(initial_config, file_config, append=False)
        config = deep_merge(config, env_config, append=False)
        config = deep_merge(config, namespace_config, append=False)

        return cls(**config)
