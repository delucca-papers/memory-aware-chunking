import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os


def read_data(file_path):
    return pd.read_csv(file_path)


def preprocess_data(data):
    data["Number of Inlines"] = data["Dataset Shape"].apply(
        lambda x: int(x.split("-")[0])
    )
    return data[data["Event"] == "EXECUTED_ATTRIBUTE"]


def aggregate_data(filtered_data):
    return (
        filtered_data.groupby(["Attribute", "Number of Inlines"])["Memory Usage (kB)"]
        .mean()
        .reset_index()
    )


def generate_line_plot(aggregate_data, directory_path):
    plt.figure(figsize=(10, 6))
    for attribute in aggregate_data["Attribute"].unique():
        subset = aggregate_data[aggregate_data["Attribute"] == attribute]
        plt.plot(
            subset["Number of Inlines"],
            subset["Memory Usage (kB)"],
            marker="o",
            label=attribute,
        )

    plt.xlabel("Number of Inlines")
    plt.ylabel("Average Memory Usage (kB)")
    plt.title("Average Memory Usage by Attribute and Number of Inlines")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(directory_path, "memory_usage_summary_line_plot.png"))
    plt.close()


def generate_box_plot(data, directory_path):
    plt.figure(figsize=(12, 8))
    sns.boxplot(
        x="Number of Inlines", y="Memory Usage (kB)", hue="Attribute", data=data
    )
    plt.title("Memory Usage Variability by Attribute and Number of Inlines")
    plt.savefig(os.path.join(directory_path, "box_plot_memory_usage.png"))
    plt.close()


def generate_heatmap(data, directory_path):
    pivot_table = data.pivot_table(
        values="Memory Usage (kB)",
        index="Attribute",
        columns="Number of Inlines",
        aggfunc="mean",
    )
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt=",.0f", cmap="viridis")
    plt.title("Heatmap of Average Memory Usage (kB)")
    plt.savefig(os.path.join(directory_path, "heatmap_average_memory_usage.png"))
    plt.close()


def generate_scatter_plot(data, directory_path):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        x="Number of Inlines",
        y="Memory Usage (kB)",
        hue="Attribute",
        style="Attribute",
        data=data,
    )
    plt.title("Memory Usage vs. Number of Inlines Scatter Plot")
    plt.savefig(os.path.join(directory_path, "scatter_plot_memory_usage.png"))
    plt.close()


if __name__ == "__main__":
    directory_path = sys.argv[1]
    file_path = os.path.join(directory_path, "memory_usage_report.csv")

    data = read_data(file_path)
    processed_data = preprocess_data(data)
    aggregated_data = aggregate_data(processed_data)

    generate_line_plot(aggregated_data, directory_path)
    generate_box_plot(processed_data, directory_path)
    generate_heatmap(aggregated_data, directory_path)
    generate_scatter_plot(processed_data, directory_path)
