import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from matplotlib.ticker import AutoLocator
from dowser.profiler.report import ProfilerReport

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


def plot_memory_usage_by_backend(directory: str):
    dataframes = {
        "psutil": __get_memory_usage_results(directory, "psutil"),
        "resource": __get_memory_usage_results(directory, "resource"),
        "mprof": __get_memory_usage_results(directory, "mprof"),
        "tracemalloc": __get_memory_usage_results(directory, "tracemalloc"),
        "kernel": __get_memory_usage_results(directory, "kernel"),
        "fil": __get_fil_memory_usage_results(directory),
    }

    largest_length = max([len(df) for df in dataframes.values()])
    unit = dataframes["psutil"]["unit"][0]
    inputs = dataframes["psutil"]["inputs"][0]
    inputs = __get_input_shape(inputs)

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
    plt.title(f"Memory Usage Over Time by Backend ({inputs})", **title_kwargs)
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
        "fil": __get_execution_time_result(directory, "fil"),
    }

    inputs = data["psutil"][1]
    sorted_data = [
        (backend, value[0])
        for backend, value in sorted(data.items(), key=lambda item: item[1])
    ]

    backends = [backend for backend, _ in sorted_data]
    values = [value for _, value in sorted_data]

    bars = plt.bar(backends, values, color="gray")

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
    plt.title(
        f"Performance Comparison of Different Libraries ({inputs})", **title_kwargs
    )
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    plt.savefig(os.path.join(directory, "execution-time-comparisson.png"))
    plt.clf()


def __get_execution_time_result(directory: str, backend: str):
    backend_report = __get_result_file_report(directory, backend)
    time_profile = backend_report.get_profiles_by_metric("time")[0]
    inputs = time_profile.get("metadata").get("inputs")
    inputs = __get_input_shape(inputs)

    execution_time_entry = list(
        filter(
            lambda entry: entry.get("event_type") == "EXECUTION_TIME",
            time_profile.get("entries"),
        )
    )
    execution_time = execution_time_entry[0].get("time")

    return float(execution_time), inputs


def __get_input_shape(inputs: str) -> str:
    return f"shape=({','.join(inputs.split(';')[0].split('=')[1].split('/')[-1].split('.')[0].split('-'))})"


def __get_memory_usage_results(directory: str, backend: str) -> pd.DataFrame:
    backend_report = __get_result_file_report(directory, backend)
    memory_usage_profile = backend_report.get_profiles_by_metric("memory_usage")[0]

    unit = memory_usage_profile.get("metadata").get("unit")
    inputs = memory_usage_profile.get("metadata").get("inputs")
    memory_usage_log = [
        entry.get("memory_usage") for entry in memory_usage_profile.get("entries")
    ]

    return pd.DataFrame(
        {
            "current_memory_usage": memory_usage_log,
            "unit": unit,
            "inputs": inputs,
        },
    )


def __get_fil_memory_usage_results(directory: str) -> pd.DataFrame:
    fil_report = open(os.path.join(directory, "fil/peak-memory.prof"), "r")
    inputs = __get_execution_time_result(directory, "fil")[1]
    unit = "mb"

    memory_usage_log = [
        int(line.split(" ")[-1]) / 1024**2 for line in fil_report.readlines()
    ]

    for i in range(1, len(memory_usage_log)):
        memory_usage_log[i] += memory_usage_log[i - 1]

    return pd.DataFrame(
        {
            "current_memory_usage": memory_usage_log,
            "unit": unit,
            "inputs": inputs,
        },
    )


def __get_result_file_report(directory: str, backend: str) -> ProfilerReport:
    output_dir = os.path.join(directory, backend)
    output_files = os.listdir(output_dir)
    profiler_filepaths = list(filter(lambda x: f"profiles" in x, output_files))

    if len(profiler_filepaths) > 1:
        raise RuntimeError("More than one memory usage result file found")
    if len(profiler_filepaths) == 0:
        raise RuntimeError("No memory usage result file found")

    backend_profile_filepath = os.path.join(output_dir, profiler_filepaths[0])

    return ProfilerReport.from_filepath(backend_profile_filepath)


if __name__ == "__main__":
    directory_path = os.environ.get("EXPERIMENT_OUTPUT_DIR")

    plot_memory_usage_by_backend(directory_path)
    plot_execution_time_by_backend(directory_path)
