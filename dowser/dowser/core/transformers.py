from .logging import get_logger


def convert_to(unit_to: str, unit_from: str, value: float) -> float:
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

    conversion_key = f"{unit_from.lower()}_to_{unit_to.lower()}"
    if conversion_key not in conversion:
        logger = get_logger()
        logger.error(f"Conversion from {unit_from} to {unit_to} is not supported")
        return value

    return float(value / conversion[conversion_key])


__all__ = ["convert_to"]
