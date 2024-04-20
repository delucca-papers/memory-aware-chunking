from toolz import curry


def convert_to(unit_to: str, unit_from: str, value: float) -> float:
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


@curry
def format_float(
    decimal_places: int,
    zfill: int,
    zfill_character: str,
    value: float,
) -> str:
    formatted = f"{value:.{decimal_places}f}"

    return formatted.rjust(zfill + decimal_places, zfill_character)


def align_tuples(tuples: list[tuple]) -> list[tuple]:
    max_length = max(len(first) for first, _ in tuples)

    formatted_tuples = []
    for first, second in tuples:
        padded_first = f"{first:{max_length}}\t"
        formatted_tuples.append((padded_first, second))

    return formatted_tuples


@curry
def deep_merge(old_dict: dict, new_dict: dict) -> dict:
    merged = dict(old_dict)

    for key, value in new_dict.items():
        if key in old_dict and isinstance(value, dict):
            merged[key] = deep_merge(old_dict[key], value)
        elif value:
            merged[key] = value

    return merged


__all__ = ["convert_to", "format_float", "align_tuples", "deep_merge"]
