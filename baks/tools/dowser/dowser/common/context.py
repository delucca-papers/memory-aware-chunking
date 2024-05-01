import os
import toml

from abc import ABC
from typing import Any

from .transformers import deep_merge


class Context(ABC):
    _base_path: str = ""
    _initial_data: dict = {}
    _data: dict = {}

    def __init__(
        self,
        initial_data,
        config_file: str = os.environ.get("DOWSER_CONFIG_FILE", "dowser.toml"),
    ):
        initial_data = initial_data or self._initial_data

        self.update(initial_data)
        self.__load_config_file(config_file)
        self.__override_with_env()

    def get(self, path: str, type: Any = None) -> Any:
        path_parts = path.split(".")
        value = self._data

        for key in path_parts:
            if key in value:
                value = value[key]
            else:
                return None

        if type:
            value = type(value)

        return value

    def set(self, path: str, value: Any) -> None:
        path_parts = path.split(".")
        final_key = path_parts[-1]
        path_parts = path_parts[:-1]
        data = self._data

        for key in path_parts:
            if key not in data:
                data[key] = {}

            data = data[key]

        data[final_key] = value

    def update(self, new_data: dict) -> None:
        self._data = deep_merge(self._data, new_data)

    def as_dict(self) -> dict:
        return self._data

    def __load_config_file(self, config_file: str) -> None:
        try:
            config_file = open(config_file, "r")
            loaded_config = toml.load(config_file)
        except Exception as e:
            return

        loaded_config = loaded_config.get(self._base_path, {})
        self.update(loaded_config)

    def __override_with_env(self, config=None, parent_key: str = ""):
        config = config or self._data

        for key, value in config.items():
            env_var = (parent_key + "_" + key if parent_key else key).upper()
            prefixed_env_var = f"DOWSER_{self._base_path.upper()}_{env_var}"

            if isinstance(value, dict):
                self.__override_with_env(value, parent_key=env_var)
            else:
                if prefixed_env_var in os.environ:
                    config[key] = os.getenv(prefixed_env_var)


__all__ = ["Context"]
