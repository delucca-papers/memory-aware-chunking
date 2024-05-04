import pandas as pd
import numpy as np

from typing import Union, Any, List
from toolz import curry
from dowser.common.transformers import convert_to_unit


__all__ = [
    "explode_additional_data",
    "to_unit",
    "to_memory_usage_evolution",
]


def to_memory_usage_evolution(
    profile: pd.DataFrame,
    columns_to_keep: List[str] = ["timestamp", "value", "unit"],
) -> pd.DataFrame:
    memory_usage_profile = profile[profile["metric"] == "MEMORY_USAGE"].copy()

    memory_usage_profile["timestamp"] = pd.to_datetime(
        memory_usage_profile["timestamp"],
        unit="s",
    )
    memory_usage_profile.sort_values("timestamp", inplace=True)

    memory_usage_profile["value"] = pd.to_numeric(memory_usage_profile["value"])
    columns_to_drop = set(memory_usage_profile.columns) - set(columns_to_keep)

    return memory_usage_profile.drop(columns=columns_to_drop)


@curry
def column_to_unit(metric: str, unit: str, profile: pd.DataFrame) -> pd.DataFrame:
    mask = profile["metric"] == metric
    for index, row in profile[mask].iterrows():
        profile.at[index, "value"] = convert_to_unit(
            unit, row["unit"], float(row["value"])
        )
        profile.at[index, "unit"] = unit

    return profile


def explode_additional_data(profile: pd.DataFrame) -> pd.DataFrame:
    exploded_profile = profile.explode("additional_data")

    new_data = {
        "metric": exploded_profile["additional_data"].map(from_additional_data(0)),
        "value": exploded_profile.apply(
            lambda d: from_additional_data(
                1,
                d["additional_data"],
                default_value=d["timestamp"],
            ),
            axis=1,
        ),
        "unit": exploded_profile.apply(
            lambda d: from_additional_data(
                2,
                d["additional_data"],
                "s",
            ),
            axis=1,
        ),
    }

    exploded_profile = exploded_profile.assign(**new_data)
    exploded_profile.drop(columns="additional_data")

    return exploded_profile.reset_index(drop=True)


@curry
def from_additional_data(
    index: int,
    row: np.ndarray,
    default_value: Any = None,
) -> Union[str, float]:
    if len(row) <= index:
        return default_value

    return row[index]
