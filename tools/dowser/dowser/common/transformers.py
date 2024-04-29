from toolz import curry


__all__ = ["unique", "deep_merge", "filter_defined_values", "str_as_list"]


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


def filter_defined_values(data: dict) -> dict:
    if not isinstance(data, dict):
        return data

    filtered_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            nested = filter_defined_values(value)
            if nested:
                filtered_data[key] = nested
        elif value is not None:
            filtered_data[key] = value

    return filtered_data


def str_as_list(value: str, sep: str = ",") -> list:
    return [part for part in value.split(sep) if part and part != ""]
