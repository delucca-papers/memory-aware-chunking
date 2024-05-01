import re

from toolz import curry
from typing import Literal


@curry
def deep_merge(old_dict: dict, new_dict: dict) -> dict:
    merged = dict(old_dict)

    for key, value in new_dict.items():
        if key in old_dict and isinstance(value, dict):
            merged[key] = deep_merge(old_dict[key], value)
        elif key in old_dict and isinstance(value, list):
            merged[key] = old_dict[key] + value
        else:
            merged[key] = value

    return merged


def standardize_key(key: str):
    key = re.sub(r"[^a-zA-Z0-9]", " ", key)
    key = key.lower()
    return key


def to_camel_case(s: str) -> str:
    words = standardize_key(s).split()
    return words[0] + "".join(word.capitalize() for word in words[1:])


def to_snake_case(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def normalize_keys_case(
    obj,
    to_case: Literal["camel", "snake"] = "snake",
):
    available_converters = {
        "camel": to_camel_case,
        "snake": to_snake_case,
    }
    convert = available_converters[to_case]

    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            new_key = convert(key)
            new_dict[new_key] = normalize_keys_case(value, to_case=to_case)
        return new_dict
    elif isinstance(obj, list):
        return [normalize_keys_case(item, to_case=to_case) for item in obj]
    else:
        return obj


def convert_to_unit(unit_to: str, unit_from: str, value: float) -> float:
    normalized_unit_to = unit_to.lower()
    normalized_unit_from = unit_from.lower()

    if normalized_unit_to == normalized_unit_from:
        return value

    conversion = {
        "b_to_kb": 1024,
        "b_to_mb": 1024**2,
        "b_to_gb": 1024**3,
        "kb_to_b": 1 / 1024,
        "kb_to_mb": 1024,
        "kb_to_gb": 1024**2,
        "mb_to_b": 1 / 1024**2,
        "mb_to_kb": 1 / 1024,
        "mb_to_gb": 1024,
        "gb_to_b": 1 / 1024**3,
        "gb_to_kb": 1 / 1024**2,
        "gb_to_mb": 1 / 1024,
    }

    conversion_key = f"{normalized_unit_from}_to_{normalized_unit_to}"
    if conversion_key not in conversion:
        raise ValueError(f"Conversion from {unit_from} to {unit_to} is not supported")

    return float(value / conversion[conversion_key])


def args_to_str(args: dict) -> str:
    normalized_args = []

    for key, value in args.items():
        normalized_args.append(f"{key}={value}")

    return ";".join(normalized_args)


__all__ = ["deep_merge", "normalize_keys_case", "convert_to_unit", "args_to_str"]
