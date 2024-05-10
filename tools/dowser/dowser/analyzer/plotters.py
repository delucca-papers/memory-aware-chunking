import pandas as pd
import plotly.graph_objects as go

from dowser.common.logger import logger
from dowser.common.transformers import convert_to_unit


__all__ = ["plot_memory_usage_comparison", "plot_execution_time_comparison"]


def plot_memory_usage_comparison(data_dict: dict, output_dir: str) -> None:
    logger.info("Plotting memory usage comparison")
    fig = go.Figure()

    if data_dict:
        sample_data = next(iter(data_dict.values()))
        metadata = sample_data.attrs.get("metadata", {})
        metadata_str = ", ".join(f"{key}={value}" for key, value in metadata.items())
    else:
        metadata_str = "No metadata available"

    for name, data in data_dict.items():
        logger.debug(f"Plotting for {name}")
        unit = data.iloc[0]["unit"].upper()

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["value"],
                mode="lines",
                name=name,
            )
        )

    fig.update_layout(
        title="Memory Usage Comparison",
        xaxis_title="Sample Index",
        yaxis_title=f"Memory Usage ({unit})",
        font=dict(family="Courier New, monospace", size=12),
        margin=dict(l=30, r=30, t=30, b=30),
        legend=dict(
            x=0.01,
            y=0.99,
            bordercolor="Black",
            borderwidth=1,
            bgcolor="rgba(255, 255, 255, 0.8)",
        ),
    )

    fig.add_annotation(
        x=0.5,
        y=0,
        xref="paper",
        yref="paper",
        text=metadata_str,
        showarrow=False,
        font=dict(family="Courier New, monospace", size=12),
        align="center",
        bgcolor="rgba(255, 255, 255, 0.8)",
    )

    logger.debug(f"Saving memory usage comparison plot to {output_dir}")
    fig.write_image(f"{output_dir}/plotted-memory-usage-comparison.png")


def plot_execution_time_comparison(data_dict: dict, output_dir: str) -> None:
    logger.info("Plotting execution time for each dataset")

    fig = go.Figure()

    if data_dict:
        sample_data = next(iter(data_dict.values()))
        metadata = sample_data.attrs.get("metadata", {})
        metadata_str = ", ".join(f"{key}={value}" for key, value in metadata.items())
    else:
        metadata_str = "No metadata available"

    execution_times = {}

    for name, data in data_dict.items():
        execution_time = data["unix_timestamp"].max() - data["unix_timestamp"].min()
        execution_time_in_seconds = convert_to_unit(
            "s",
            data.attrs["unix_timestamp_unit"],
            execution_time,
        )
        execution_times[name] = execution_time_in_seconds

    sorted_execution_times = sorted(execution_times.items(), key=lambda item: item[1])

    for name, execution_time_seconds in sorted_execution_times:
        fig.add_trace(go.Bar(x=[name], y=[execution_time_seconds], name=name))

    fig.update_layout(
        title="Execution Time for Each Dataset",
        xaxis_title="Dataset",
        yaxis_title="Execution Time (seconds)",
        font=dict(family="Courier New, monospace", size=12),
        margin=dict(l=30, r=30, t=30, b=30),
        showlegend=False,
    )

    fig.add_annotation(
        x=0.5,
        y=1,
        xref="paper",
        yref="paper",
        text=metadata_str,
        showarrow=False,
        font=dict(family="Courier New, monospace", size=12),
        align="center",
        bgcolor="rgba(255, 255, 255, 0.8)",
    )

    logger.debug(f"Saving execution time comparison plot to {output_dir}")
    fig.write_image(f"{output_dir}/plotted-execution-time-comparison.png")
