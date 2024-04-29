from toolz import curry
from enum import Enum


__all__ = [
    "unique",
    "deep_merge",
    "filter_defined_values",
    "str_as_list",
    "readable_enum_list",
]


def unique(values: list) -> list:
    unique_values = []
    for value in values:
        if value not in unique_values:
            unique_values.append(value)

    return unique_values


@curry
def deep_merge(old_dict: dict, new_dict: dict, append: bool = True) -> dict:
    merged = dict(old_dict)

    for key, value in new_dict.items():
        if key in old_dict and isinstance(value, dict):
            merged[key] = deep_merge(old_dict[key], value, append=append)
        elif key in old_dict and isinstance(value, list) and append:
            merged[key] = old_dict[key] + value
        elif value and value != "":
            merged[key] = value

    return merged


def filter_defined_values(data: dict, allow_empty_lists: bool = True) -> dict:
    if not isinstance(data, dict):
        return data

    filtered_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            nested = filter_defined_values(value, allow_empty_lists=allow_empty_lists)
            if nested:
                filtered_data[key] = nested
        elif isinstance(value, list):
            if len(value) > 0 or allow_empty_lists:
                filtered_data[key] = value
        elif value is not None:
            filtered_data[key] = value

    return filtered_data


def str_as_list(value: str | None, sep: str = ",") -> list:
    if not value:
        return []
    return [part for part in value.split(sep) if part and part != ""]


def readable_enum_list(enum_list: list[Enum]) -> str:
    return [enum.value for enum in enum_list]
