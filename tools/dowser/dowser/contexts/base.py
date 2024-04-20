from abc import ABC
from typing import Any
from ..core.transformers import deep_merge


class Context(ABC):
    _data: dict

    def __init__(self, data: dict = {}):
        self.__data = deep_merge(self._data, data)

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

    def lazy_get(self, path: str, *args, **kwargs):
        return lambda: self.get(path, *args, **kwargs)

    def update(self, new_data: dict) -> None:
        self._data = deep_merge(self._data, new_data)
