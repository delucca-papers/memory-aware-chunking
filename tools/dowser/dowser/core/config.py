import os
import uuid
import toml

from typing import Any
from .transformers import deep_merge


class Config:
    __data: dict = {
        "execution_id": str(uuid.uuid4()),
        "output_dir": "./dowser",
        "logging": {
            "level": "info",
            "filename": "dowser.log",
            "transports": "console,file",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "report": {
            "prepend_timestamp": "true",
        },
        "input": {
            "metadata": "",
        },
        "profiler": {
            "output_dir": "profiler",
            "enabled_profilers": "time,memory_usage",
            "time": {
                "report": {
                    "filename": "time",
                    "prefix": "",
                    "suffix": "",
                },
            },
            "memory_usage": {
                "backend": "mprof",
                "precision": "4",
                "report": {
                    "unit": "mb",
                    "filename": "memory-usage",
                    "prefix": "",
                    "suffix": "",
                    "decimal_places": "2",
                    "zfill": "6",
                    "zfill_character": " ",
                },
            },
        },
    }

    def __init__(
        self,
        config: dict = {},
        config_file: str = os.environ.get("DOWSER_CONFIG_FILE", "dowser.toml"),
    ):
        self.__data = deep_merge(self.__data, config)
        self.__load_config_file(config_file)
        self.__override_with_env()

    def get(self, path: str, type: Any = None) -> Any:
        path_parts = path.split(".")
        value = self.__data

        for key in path_parts:
            if key in value:
                value = value[key]
            else:
                return None

        if type:
            value = type(value)

        return value

    def lazy_get(self, path: str, *args, **kwargs):
        return lambda: self.get(path, *args, **kwargs)

    def update(self, new_config: dict) -> None:
        self.__data = deep_merge(self.__data, new_config)

    def __load_config_file(self, config_file: str) -> None:
        try:
            config_file = open(config_file, "r")
            loaded_config = toml.load(config_file)
        except Exception as e:
            return

        self.update(loaded_config)

    def __override_with_env(self, config: dict | None = None, parent_key: str = ""):
        config = config or self.__data

        for key, value in config.items():
            env_var = (parent_key + "_" + key if parent_key else key).upper()
            prefixed_env_var = f"DOWSER_{env_var}"

            if isinstance(value, dict):
                self.__override_with_env(value, parent_key=env_var)
            else:
                if prefixed_env_var in os.environ:
                    config[key] = os.getenv(prefixed_env_var)


####


config = Config()


__all__ = ["config"]
