import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from matplotlib.ticker import AutoLocator


def plot_memory_usage_by_experiment(directory: str, unit: str):
    dataframes = {
        "psutil": __get_results(directory, "psutil"),
        "resource": __get_results(directory, "resource"),
        "mprof": __get_results(directory, "mprof"),
        "tracemalloc": __get_results(directory, "tracemalloc"),
        "kernel": __get_results(directory, "kernel"),
    }

    largest_length = max([len(df) for df in dataframes.values()])

    plt.figure(figsize=(12, 6))

    for name, df in dataframes.items():
        df_length = len(df)
        new_indices = np.linspace(0, df_length - 1, num=largest_length, endpoint=True)
        interp_func = interp1d(
            np.arange(df_length),
            df["current_memory_usage"].values,
            kind="linear",
        )
        interp_current_mem_usage = interp_func(new_indices)
        plt.plot(range(0, largest_length), interp_current_mem_usage, label=name)

    plt.xlabel("Normalized Time")
    plt.ylabel(f"Memory Usage ({unit})")
    plt.title("Memory Usage Over Time by Backend")
    plt.legend()
    plt.grid(True)
    ax = plt.gca()
    ax.yaxis.set_major_locator(AutoLocator())
    plt.tight_layout()

    plt.savefig(os.path.join(directory, "memory_usage_comparison.png"))


def __get_results(directory: str, backend: str, heading_lines: int = 6) -> pd.DataFrame:
    backend_memory_usage_result_files = os.listdir(
        os.path.join(directory, backend, "memory_usage")
    )
    if len(backend_memory_usage_result_files) > 1:
        raise RuntimeError("More than one memory usage result file found")
    if len(backend_memory_usage_result_files) == 0:
        raise RuntimeError("No memory usage result file found")

    backend_memory_usage_result = open(
        os.path.join(
            directory, backend, "memory_usage", backend_memory_usage_result_files[0]
        ),
        "r",
    )

    lines = backend_memory_usage_result.readlines()
    data = lines[heading_lines:]
    timestamp_list = []
    current_memory_usage_list = []
    peak_memory_usage_list = []

    for line in data:
        line_parts = line.split("\t")
        filtered_line_parts = filter(lambda x: x != "", line_parts)
        cleaned_line_parts = map(
            lambda x: x.strip().replace("\n", ""), filtered_line_parts
        )
        line_parts_values = map(lambda x: float(x.split(" ")[1]), cleaned_line_parts)

        timestamp, current_memory_usage, peak_memory_usage = line_parts_values

        timestamp_list.append(timestamp)
        current_memory_usage_list.append(current_memory_usage)
        peak_memory_usage_list.append(peak_memory_usage)

    return pd.DataFrame(
        {
            "timestamp": timestamp_list,
            "current_memory_usage": current_memory_usage_list,
            "peak_memory_usage": peak_memory_usage_list,
        },
    )


if __name__ == "__main__":
    directory_path = os.environ.get("OUTPUT_DIR")
    unit = os.environ.get("UNIT")

    plot_memory_usage_by_experiment(directory_path, unit)
