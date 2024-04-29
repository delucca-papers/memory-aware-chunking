import os
import toml

from argparse import Namespace
from uuid import uuid4
from .transformers import deep_merge, filter_defined_values, str_as_list


__all__ = ["Config"]


class Config:
    __config_filename: str = os.environ.get("DOWSER_CONFIG", "dowser.toml")
    __data = {
        "output_dir": "./",
        "logger": {
            "enabled_transports": ["console", "file"],
            "level": "INFO",
        },
        "profiler": {
            "session_id": str(uuid4()),
            "enabled_metrics": ["memory_usage", "time"],
            "script": "",
            "args": [],
            "memory_usage": {
                "enabled_backends": ["kernel"],
                "unit": "mb",
            },
        },
    }

    @classmethod
    def from_namespace(cls, namespace: Namespace) -> "Config":
        namespace_config = filter_defined_values(
            {
                "output_dir": namespace.output_dir,
                "logger": {
                    "enabled_transports": namespace.log_transport,
                    "level": namespace.log_level,
                },
                "profiler": {
                    "session_id": namespace.session_id,
                    "enabled_metrics": namespace.enabled_metrics,
                    "script": namespace.script,
                    "args": namespace.args,
                    "memory_usage": {
                        "enabled_backends": namespace.memory_usage_enabled_backends,
                        "unit": namespace.memory_usage_unit,
                    },
                },
            }
        )

        return cls(namespace_config)

    def __init__(self, config: dict = {}):
        self.__load()
        self.__inject_env()
        self.__update(config, append=False)

    def get(self, path: str, type: any = None, value: dict | None = None) -> any:
        path_parts = path.split(".")
        value = value or self.__data

        for key in path_parts:
            if key in value:
                value = value[key]
            else:
                return None

        if type:
            value = type(value)

        return value

    def __update(self, new_data: dict, append: bool = True) -> None:
        self.__data = deep_merge(self.__data, new_data, append=append)

    def __load(self) -> None:
        try:
            config_file = open(self.__config_filename, "r")
            loaded_config = toml.load(config_file)
        except Exception as e:
            return

        loaded_config = filter_defined_values(
            {
                "output_dir": loaded_config.get("output_dir"),
                "logger": {
                    "enabled_transports": self.get(
                        "logger.enabled_transports",
                        value=loaded_config,
                        type=str_as_list,
                    ),
                    "level": self.get("logger.level", value=loaded_config),
                },
                "profiler": {
                    "session_id": self.get("profiler.session_id", value=loaded_config),
                    "enabled_metrics": self.get(
                        "profiler.enabled_metrics",
                        value=loaded_config,
                        type=str_as_list,
                    ),
                    "script": self.get("profiler.script", value=loaded_config),
                    "args": self.get(
                        "profiler.args",
                        value=loaded_config,
                        type=str_as_list,
                    ),
                    "memory_usage": {
                        "enabled_backends": self.get(
                            "profiler.memory_usage.enabled_backends",
                            value=loaded_config,
                            type=str_as_list,
                        ),
                        "unit": self.get(
                            "profile.memory_usage.unit",
                            value=loaded_config,
                        ),
                    },
                },
            }
        )

        self.__update(loaded_config, append=False)

    def __inject_env(self, config: dict | None = None, parent_key: str = ""):
        config = config or self.__data

        for key, value in config.items():
            env_var = (parent_key + "_" + key if parent_key else key).upper()
            prefixed_env_var = f"DOWSER_{env_var}"

            if isinstance(value, dict):
                self.__inject_env(value, parent_key=env_var)
            else:
                if prefixed_env_var in os.environ:
                    config[key] = os.getenv(prefixed_env_var)

    def __str__(self) -> str:
        return str(self.__data)
