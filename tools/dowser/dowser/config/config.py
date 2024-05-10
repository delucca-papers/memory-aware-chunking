import os
import toml

from pydantic import BaseModel, DirectoryPath, field_validator
from argparse import Namespace
from dowser.common.transformers import (
    filter_defined_values,
    str_as_list,
    deep_merge,
    from_key_value_string,
)
from .logger import LoggerConfig
from .profiler import ProfilerConfig
from .analyzer import AnalyzerConfig


__all__ = ["Config"]

initial_config = {
    "output_dir": "./",
    "logger": {
        "enabled_transports": ["CONSOLE"],
        "level": "INFO",
    },
    "profiler": {
        "enabled_metrics": ["MEMORY_USAGE", "TIME"],
        "depth": "3",
        "memory_usage": {
            "enabled_backends": ["KERNEL"],
        },
    },
    "analyzer": {
        "unit": "mb",
    },
}


class Config(BaseModel):
    output_dir: DirectoryPath
    logger: LoggerConfig
    profiler: ProfilerConfig
    analyzer: AnalyzerConfig

    @field_validator("output_dir", mode="before")
    def create_dir_if_not_exists(cls, v):
        if not os.path.isdir(v):
            os.makedirs(v, exist_ok=True)
        return v

    @staticmethod
    def parse_env() -> dict:
        return filter_defined_values(
            {
                "profiler_session_id": os.environ.get("DOWSER_PROFILER_SESSION_ID"),
                "output_dir": os.environ.get("DOWSER_OUTPUT_DIR"),
                "log_level": os.environ.get("DOWSER_LOG_LEVEL"),
                "log_transport": str_as_list(os.environ.get("DOWSER_LOG_TRANSPORT")),
                "enable_metric": str_as_list(os.environ.get("DOWSER_ENABLE_METRIC")),
                "unit": os.environ.get("DOWSER_UNIT"),
                "profiler_depth": os.environ.get("DOWSER_PROFILER_DEPTH"),
                "enable_mem_backend": str_as_list(
                    os.environ.get("DOWSER_ENABLE_MEM_BACKEND")
                ),
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
                "analyzer": {
                    **loaded_config.get("analyzer", {}),
                    "sessions": from_key_value_string(loaded_config.get("session")),
                },
            },
            allow_empty_lists=False,
        )

    @staticmethod
    def from_flat_config(flat_config: dict) -> dict:
        return filter_defined_values(
            {
                "output_dir": flat_config.get("output_dir"),
                "logger": {
                    "enabled_transports": flat_config.get("log_transport"),
                    "level": flat_config.get("log_level"),
                },
                "profiler": {
                    "session_id": flat_config.get("profiler_session_id"),
                    "depth": flat_config.get("profiler_depth"),
                    "enabled_metrics": flat_config.get("enable_metric"),
                    "filepath": flat_config.get("filepath"),
                    "entrypoint": flat_config.get("entrypoint"),
                    "args": flat_config.get("args"),
                    "kwargs": [
                        kwarg
                        for kwarg_list in flat_config.get("kwargs", [])
                        for kwarg in kwarg_list
                    ],
                    "memory_usage": {
                        "enabled_backends": flat_config.get("enable_mem_backend"),
                    },
                },
                "analyzer": {
                    "unit": flat_config.get("unit"),
                    "sessions": from_key_value_string(flat_config.get("session")),
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

    @classmethod
    def from_initial_config(cls, custom_config: dict = initial_config) -> "Config":
        env_config = cls.from_flat_config(cls.parse_env())
        file_config = cls.parse_file()

        config = deep_merge(custom_config, file_config, append=False)
        config = deep_merge(config, env_config, append=False)

        return cls(**config)
