import toml
import os

from typing import Any
from .constants import DEFAULT_CONFIG_FILE, DEFAULT_CONFIG


def _load_config(file_path: str = DEFAULT_CONFIG_FILE) -> dict:
    try:
        config_file = open(file_path, "r")
        config = toml.load(config_file)
    except Exception as e:
        config = DEFAULT_CONFIG

    config = _override_with_env(config)
    return {
        **DEFAULT_CONFIG,
        **config,
    }


def _override_with_env(config: dict, parent_key: str = "") -> dict:
    for key, value in config.items():
        env_var = (parent_key + "_" + key if parent_key else key).upper()

        if isinstance(value, dict):
            config[key] = _override_with_env(value, parent_key=env_var)
        else:
            if env_var in os.environ:
                config[key] = os.getenv(env_var)

    return config


class ConfigManager:
    __config: dict = _load_config()

    def __init__(self, file_path: str = DEFAULT_CONFIG_FILE):
        if file_path != DEFAULT_CONFIG_FILE:
            self.__config = _load_config(file_path)

    def get_config(self, path: str, type: Any = None) -> Any:
        keys = path.split(".")
        value = self.__config

        for key in keys:
            if key in value:
                value = value[key]
            else:
                return None

        return type(value) if type else value

    def update_config(self, config: dict, path: str) -> None:
        keys = path.split(".")
        value = self.__config

        for key in keys:
            value = value[key]

        value.update(config)
