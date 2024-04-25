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


__all__ = ["deep_merge"]
