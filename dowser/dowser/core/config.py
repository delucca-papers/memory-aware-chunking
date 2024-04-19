import os
import uuid
import toml

from typing import Any
from toolz import compose, curry, merge_with

DEFAULT_CONFIG_FILE = os.environ.get(f"DOWSER_CONFIG_FILE", "dowser.toml")
DEFAULT_CONFIG = {
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
        "enabled_profilers": "execution_time,memory_usage",
        "execution_time": {
            "report": {
                "filename": "execution-time",
                "prefix": "",
                "suffix": "",
            },
        },
        "memory_usage": {
            "backend": "kernel",
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


####


def load_config_file(config_file: str = DEFAULT_CONFIG_FILE) -> dict:
    try:
        config_file = open(config_file, "r")
        config = toml.load(config_file)
    except Exception as e:
        config = DEFAULT_CONFIG

    return deep_merge(DEFAULT_CONFIG, config)


def override_with_env(config: dict, parent_key: str = "") -> dict:
    for key, value in config.items():
        env_var = (parent_key + "_" + key if parent_key else key).upper()
        prefixed_env_var = f"DOWSER_{env_var}"

        if isinstance(value, dict):
            config[key] = override_with_env(value, parent_key=env_var)
        else:
            if prefixed_env_var in os.environ:
                config[key] = os.getenv(prefixed_env_var)

    return config


@curry
def deep_merge(old_dict: dict, new_dict: dict) -> dict:
    merged = dict(old_dict)

    for key, value in new_dict.items():
        if key in old_dict and isinstance(value, dict):
            merged[key] = deep_merge(old_dict[key], value)
        elif value:
            merged[key] = value

    return merged


def parts_from_path(path: str) -> list[str]:
    return path.split(".")


@curry
def get_from_path_parts(config: dict, path_parts: list[str]) -> Any:
    value = config

    for key in path_parts:
        if key in value:
            value = value[key]
        else:
            return None

    return value


@curry
def transform_to_type(type: Any, value: Any) -> Any:
    return type(value)


###


get_full_config = compose(
    override_with_env,
    load_config_file,
)

config = get_full_config()


def get_namespace(path: str, config: dict = config) -> dict:
    return compose(
        transform_to_type(dict),
        get_from_path_parts(config),
        parts_from_path,
    )(path)


def get_config(path: str, config: dict = config) -> Any:
    return compose(
        get_from_path_parts(config),
        parts_from_path,
    )(path)


def extend_config(new_config: dict) -> dict:
    return deep_merge(config, new_config)


__all__ = ["get_full_config", "config", "get_namespace", "get_config", "extend_config"]
