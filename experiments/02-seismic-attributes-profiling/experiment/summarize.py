import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main(output_dir: str, execution_id: str) -> None:
    experiment_output_dir = os.path.join(output_dir, execution_id)

    __generate_memory_usage_graphs(experiment_output_dir)
    # __generate_execution_time_graphs(reports_dir, graphs_dir)


def __generate_memory_usage_graphs(experiment_output_dir: str) -> None:
    pass


"""     memory_usage_report = os.path.join(reports_dir, "memory_usage_report.csv")
    data = __read_data(memory_usage_report)

    # Preprocess data
    data = __add_dimensions(data)
    data = __group_by_event(data)

    __generate_inline_memory_usage_graphs(data, output_dir)
    __generate_crossline_memory_usage_graphs(data, output_dir)


def __generate_inline_memory_usage_graphs(data: pd.DataFrame, output_dir: str) -> None:
    inline_data = data.copy()
    filtered_data = __filter_data_by_varying_dimension(
        inline_data, "Inlines", "Crosslines"
    )
    aggregated_data = __aggregate_data(filtered_data)

    __generate_line_plot(
        aggregated_data,
        output_dir,
        "Number of Inlines",
        "Memory Usage (kB)",
        "Average Memory Usage by Attribute and Number of Inlines",
    )

    __generate_heatmap(
        aggregated_data,
        output_dir,
        "Memory Usage (kB)",
        "Attribute",
        "Number of Inlines",
        "Heatmap of Average Memory Usage (kB) while varying Inlines",
    )

    __generate_scatter_plot(
        filtered_data,
        output_dir,
        "Number of Inlines",
        "Memory Usage (kB)",
        "Attribute",
        "Attribute",
        "Memory Usage vs. Number of Inlines Scatter Plot",
    )


def __generate_crossline_memory_usage_graphs(
    data: pd.DataFrame, output_dir: str
) -> None:
    crossline_data = data.copy()
    filtered_data = __filter_data_by_varying_dimension(
        crossline_data, "Crosslines", "Inlines"
    )
    aggregated_data = __aggregate_data(filtered_data)

    __generate_line_plot(
        aggregated_data,
        output_dir,
        "Number of Crosslines",
        "Memory Usage (kB)",
        "Average Memory Usage by Attribute and Number of Crosslines",
    )

    __generate_heatmap(
        aggregated_data,
        output_dir,
        "Memory Usage (kB)",
        "Attribute",
        "Number of Crosslines",
        "Heatmap of Average Memory Usage (kB) while varying Crosslines",
    )

    __generate_scatter_plot(
        filtered_data,
        output_dir,
        "Number of Crosslines",
        "Memory Usage (kB)",
        "Attribute",
        "Attribute",
        "Memory Usage vs. Number of Crosslines Scatter Plot",
    )


def __generate_execution_time_graphs(reports_dir: str, output_dir: str) -> None:
    execution_time_report = os.path.join(reports_dir, "execution_time_report.csv")
    data = __read_data(execution_time_report)

    # Preprocess data
    data = __add_dimensions(data)
    data = __add_dimension_iteration(data)
    data = __add_execution_time(data)

    __generate_inline_execution_time_graphs(data, output_dir)
    __generate_crossline_execution_time_graphs(data, output_dir)


def __generate_inline_execution_time_graphs(
    data: pd.DataFrame, output_dir: str
) -> None:
    inline_data = data.copy()
    filtered_data = __filter_data_by_varying_dimension(
        inline_data, "Inlines", "Crosslines"
    )
    aggregated_data = __aggregate_data(filtered_data)
    aggregated_data = __keep_only_first_dimension_iteration(aggregated_data)
    grouped_data = __group_by_event(aggregated_data)

    __generate_line_plot(
        grouped_data,
        output_dir,
        "Number of Inlines",
        "Execution Time (in seconds)",
        "Average Execution Time by Attribute and Number of Inlines",
    )


def __generate_crossline_execution_time_graphs(
    data: pd.DataFrame, output_dir: str
) -> None:
    inline_data = data.copy()
    filtered_data = __filter_data_by_varying_dimension(
        inline_data, "Crosslines", "Inlines"
    )
    aggregated_data = __aggregate_data(filtered_data)
    aggregated_data = __keep_only_first_dimension_iteration(aggregated_data)
    grouped_data = __group_by_event(aggregated_data)

    __generate_line_plot(
        grouped_data,
        output_dir,
        "Number of Crosslines",
        "Execution Time (in seconds)",
        "Average Execution Time by Attribute and Number of Crosslines",
    )


def __read_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def __add_dimensions(data: pd.DataFrame) -> pd.DataFrame:
    data["Number of Inlines"] = data["Dataset Shape"].apply(
        lambda x: int(x.split("-")[0])
    )
    data["Number of Crosslines"] = data["Dataset Shape"].apply(
        lambda x: int(x.split("-")[1])
    )
    data["Number of Samples"] = data["Dataset Shape"].apply(
        lambda x: int(x.split("-")[2])
    )

    return data


def __group_by_event(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby(
            [
                "Attribute",
                "Dataset Shape",
                "Event",
                "Number of Inlines",
                "Number of Crosslines",
                "Number of Samples",
            ]
        )
        .mean()
        .drop(columns=["Iteration"])
        .reset_index()
    )


def __filter_data_by_varying_dimension(
    data: pd.DataFrame,
    dimension_varying: str,
    dimension_static: str,
    inclusive: bool = True,
) -> pd.DataFrame:
    return data[
        (
            (
                data[f"Number of {dimension_varying}"]
                >= data[f"Number of {dimension_static}"]
            )
            if inclusive
            else (
                data[f"Number of {dimension_varying}"]
                > data[f"Number of {dimension_static}"]
            )
        )
    ]


def __add_dimension_iteration(data: pd.DataFrame) -> pd.DataFrame:
    data["Dimension Iteration"] = (
        data["Dataset Shape"] + "-" + data["Iteration"].astype(str)
    )

    return data


def __add_execution_time(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby("Dimension Iteration").apply(
        __calculate_execution_time,
        include_groups=False,
    )


def __calculate_execution_time(group: pd.DataFrame) -> pd.DataFrame:
    start_time = group[group["Event"] == "STARTED_EXPERIMENT"][
        "Time Since Epoch (in seconds)"
    ].values[0]
    group["Execution Time (in seconds)"] = (
        group["Time Since Epoch (in seconds)"] - start_time
    )

    return group


def __keep_only_first_dimension_iteration(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby("Dimension Iteration").apply(
        lambda x: x.head(1),
    )


def __aggregate_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[data["Event"] == "EXECUTED_ATTRIBUTE"]


def __generate_line_plot(
    data: pd.DataFrame,
    output_dir: str,
    x_axis: str,
    y_axis: str,
    title: str,
) -> None:
    kebab_title = __to_kebab(title)

    plt.figure(figsize=(10, 6))
    for attribute in data["Attribute"].unique():
        subset = data[data["Attribute"] == attribute]
        plt.plot(
            subset[x_axis],
            subset[y_axis],
            marker="o",
            label=attribute,
        )

    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{kebab_title}.png"))
    plt.close()


def __generate_heatmap(
    data: pd.DataFrame,
    output_dir: str,
    values: str,
    index: str,
    columns: str,
    title: str,
    aggfunc: str = "mean",
) -> None:
    kebab_title = __to_kebab(title)

    pivot_table = data.pivot_table(
        values=values,
        index=index,
        columns=columns,
        aggfunc=aggfunc,
    )
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt=",.0f", cmap="viridis")
    plt.title(title)
    plt.savefig(os.path.join(output_dir, f"{kebab_title}.png"))
    plt.close()


def __generate_scatter_plot(
    data: pd.DataFrame,
    output_dir: str,
    x_axis: str,
    y_axis: str,
    hue: str,
    style: str,
    title: str,
) -> None:
    kebab_title = __to_kebab(title)

    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        x="Number of Inlines",
        y="Memory Usage (kB)",
        hue="Attribute",
        style="Attribute",
        data=data,
    )
    plt.title(title)
    plt.savefig(os.path.join(output_dir, f"{kebab_title}.png"))
    plt.close()


def __to_kebab(text: str) -> str:
    return text.lower().replace(" ", "_")
 """

if __name__ == "__main__":
    execution_id = os.environ.get("EXPERIMENT_EXECUTION_ID")
    directory_path = os.environ.get("EXPERIMENT_OUTPUT_DIR")

    main(directory_path, execution_id)
