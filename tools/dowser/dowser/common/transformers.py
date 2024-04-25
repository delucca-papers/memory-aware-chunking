import re

from toolz import curry


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


def to_camel_case(s: str):
    words = standardize_key(s).split()
    return words[0] + "".join(word.capitalize() for word in words[1:])


def convert_keys_to_camel_case(obj: dict | list | str):
    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            new_key = to_camel_case(key)
            new_dict[new_key] = convert_keys_to_camel_case(value)
        return new_dict
    elif isinstance(obj, list):
        return [convert_keys_to_camel_case(item) for item in obj]
    else:
        return obj


__all__ = ["deep_merge", "convert_keys_to_camel_case"]
