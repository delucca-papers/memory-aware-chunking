import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from matplotlib.ticker import AutoLocator

axis_kwargs = {
    "fontsize": 12,
    "fontweight": "bold",
}
title_kwargs = {
    "fontsize": 14,
    "fontweight": "bold",
}

plt.figure(figsize=(12, 6))
plt.style.use("bmh")
plt.grid(True)


def plot_memory_usage_by_backend(directory: str, unit: str):
    dataframes = {
        "psutil": __get_memory_usage_results(directory, "psutil"),
        "resource": __get_memory_usage_results(directory, "resource"),
        "mprof": __get_memory_usage_results(directory, "mprof"),
        "tracemalloc": __get_memory_usage_results(directory, "tracemalloc"),
        "kernel": __get_memory_usage_results(directory, "kernel"),
    }

    largest_length = max([len(df) for df in dataframes.values()])

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

    plt.xlabel("Normalized Time", **axis_kwargs)
    plt.ylabel(f"Memory Usage (in {unit.upper()})", **axis_kwargs)
    plt.title("Memory Usage Over Time by Backend", **title_kwargs)
    plt.legend()
    ax = plt.gca()
    ax.yaxis.set_major_locator(AutoLocator())

    plt.tight_layout()
    plt.savefig(os.path.join(directory, "memory-usage-comparison.png"))
    plt.clf()


def plot_execution_time_by_backend(directory: str):
    data = {
        "psutil": __get_execution_time_result(directory, "psutil"),
        "resource": __get_execution_time_result(directory, "resource"),
        "mprof": __get_execution_time_result(directory, "mprof"),
        "tracemalloc": __get_execution_time_result(directory, "tracemalloc"),
        "kernel": __get_execution_time_result(directory, "kernel"),
    }

    sorted_data = dict(sorted(data.items(), key=lambda item: item[1]))

    bars = plt.bar(sorted_data.keys(), sorted_data.values(), color="gray")

    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            round(yval, 2),
            va="bottom",
        )

    plt.xlabel("Libraries", **axis_kwargs)
    plt.ylabel("Execution time (in seconds)", **axis_kwargs)
    plt.title("Performance Comparison of Different Libraries", **title_kwargs)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    plt.savefig(os.path.join(directory, "execution-time-comparisson.png"))
    plt.clf()


def __get_execution_time_result(directory: str, backend: str) -> float:
    backend_times_file = __get_result_file(directory, backend, "time")

    execution_time = None

    for line in backend_times_file.readlines():
        if "EXECUTION_TIME" in line:
            _, execution_time_report = line.split("\t")
            execution_time, _ = execution_time_report.strip().split(" ")
            break

    return float(execution_time)


def __get_memory_usage_results(
    directory: str,
    backend: str,
    heading_lines: int = 6,
) -> pd.DataFrame:
    backend_memory_usage_result = __get_result_file(directory, backend, "memory-usage")

    lines = backend_memory_usage_result.readlines()
    data = lines[heading_lines:]
    unit = None
    current_memory_usage_list = []

    for line in data:
        _, memory_usage_report = line.split("\t")
        memory_usage, reported_unit = memory_usage_report.strip().split(" ")

        current_memory_usage_list.append(float(memory_usage))

        if unit is None:
            unit = reported_unit

    return pd.DataFrame(
        {
            "current_memory_usage": current_memory_usage_list,
            "unit": unit,
        },
    )


def __get_result_file(directory: str, backend: str, metric: str):
    profiler_dir = os.path.join(directory, "profiler")
    profiler_files = os.listdir(profiler_dir)
    filepaths = list(filter(lambda x: f"{metric}-{backend}" in x, profiler_files))

    if len(filepaths) > 1:
        raise RuntimeError("More than one memory usage result file found")
    if len(filepaths) == 0:
        raise RuntimeError("No memory usage result file found")

    return open(
        os.path.join(profiler_dir, filepaths[0]),
        "r",
    )


if __name__ == "__main__":
    directory_path = os.environ.get("EXPERIMENT_OUTPUT_DIR")
    unit = os.environ.get("EXPERIMENT_UNIT")

    plot_memory_usage_by_backend(directory_path, unit)
    plot_execution_time_by_backend(directory_path)
