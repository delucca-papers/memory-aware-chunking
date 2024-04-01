import sys
import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_memory_usage_by_experiment(directory: str):
    data = {}

    for item in os.listdir(directory):
        subdir = os.path.join(directory, item)
        if os.path.isdir(subdir):
            csv_file = os.path.join(subdir, "results.csv")
            if os.path.exists(csv_file):
                df = pd.read_csv(csv_file)
                data[item] = {
                    "Initial Memory": df["initial_memory_usage"].iloc[0],
                    "Peak Memory": df["peak_memory_usage"].iloc[0],
                    "Final Memory": df["final_memory_used"].iloc[0],
                }

    plt.figure(figsize=(10, 6))
    memory_types = ["Initial Memory", "Peak Memory", "Final Memory"]

    for experiment, mem_usages in data.items():
        plt.plot(
            memory_types,
            [mem_usages[mem_type] for mem_type in memory_types],
            marker="o",
            label=experiment,
        )

    plt.title("Memory Usage by Experiment")
    plt.xlabel("Memory Usage Type")
    plt.ylabel("Memory Usage Value")
    plt.legend(title="Experiment", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    output_path = os.path.join(directory, "summary.jpg")
    plt.savefig(output_path, format="jpg")
    plt.close()

    print(f"Chart saved to {output_path}")


if __name__ == "__main__":
    directory_path = sys.argv[1]
    plot_memory_usage_by_experiment(directory_path)
