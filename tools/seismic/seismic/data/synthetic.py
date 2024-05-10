import numpy as np
import segyio
import os

from scipy.signal import convolve
from typing import Literal
from dowser import get_logger


def build_dataset_paths(
    num_inlines: int,
    num_crosslines: int,
    num_samples: int,
    step_size: int,
    range_size: int,
    output_dir: str,
    datasets_path: str = None,
) -> str:
    logger = get_logger()

    dataset_paths = []
    datasets_dir = f"{output_dir}/data"

    if datasets_path:
        dataset_paths = get_sorted_dataset_paths_from_dir(datasets_path)

    if not dataset_paths:
        dataset_paths = generate_and_save_for_range(
            num_inlines,
            num_crosslines,
            num_samples,
            step_size,
            range_size,
            datasets_dir,
        )

    logger.debug(f"Dataset paths: {dataset_paths}")

    return dataset_paths


def get_sorted_dataset_paths_from_dir(datasets_path: str):
    return [
        os.path.join(datasets_path, filename)
        for filename in sorted(os.listdir(datasets_path))
        if filename.endswith(".segy")
    ]


def generate_and_save_for_range(
    num_inlines: int,
    num_crosslines: int,
    num_samples: int,
    step_size: int,
    range_size: int,
    output_dir: str,
):
    logger = get_logger()

    logger.info(f"Generating synthetic data with the following parameters:")
    logger.info(f"Number of inlines: {num_inlines}")
    logger.info(f"Number of crosslines: {num_crosslines}")
    logger.info(f"Number of samples: {num_samples}")
    logger.info(f"Step size: {step_size}")
    logger.info(f"Range size: {range_size}")
    logger.info(f"Output directory: {output_dir}")

    varying_inlines = generate_varying_dimension(
        0,
        num_inlines,
        num_crosslines,
        num_samples,
        step_size,
        range_size,
        output_dir,
    )

    varying_crosslines = generate_varying_dimension(
        1,
        num_inlines,
        num_crosslines,
        num_samples,
        step_size,
        range_size,
        output_dir,
    )

    return varying_inlines + varying_crosslines


def generate_varying_dimension(
    dimension: Literal[0, 1, 2],
    num_inlines: int,
    num_crosslines: int,
    num_samples: int,
    step_size: int,
    range_size: int,
    output_dir: str,
):
    return [
        generate_and_save_synthetic_data(
            step_num * step_size if dimension == 0 else num_inlines,
            step_num * step_size if dimension == 1 else num_crosslines,
            step_num * step_size if dimension == 2 else num_samples,
            output_dir=output_dir,
        )
        for step_num in range(1, range_size + 1)
    ]


def generate_and_save_synthetic_data(
    num_inlines: int,
    num_crosslines: int,
    num_samples: int,
    dt: float = 0.004,
    frequency: int = 25,
    length: int = 250,
    output_dir: str = "/tmp/synthetic_seismic_data",
) -> str:
    logger = get_logger()

    filename = f"{num_inlines}-{num_crosslines}-{num_samples}.segy"
    filepath = os.path.join(output_dir, filename)
    if os.path.exists(filepath):
        logger.debug(
            f"Skipping generation of synthetic data for shape ({num_inlines}, {num_crosslines}, {num_samples}) as it already exists"
        )
        return filepath

    logger.debug(
        f"Generating synthetic data for shape ({num_inlines}, {num_crosslines}, {num_samples})"
    )

    reflectivity = np.random.rand(num_samples) * 2 - 1
    wavelet = __ricker_wavelet(frequency, length, dt)

    seismic_data = np.array(
        [
            __generate_synthetic_seismic(
                reflectivity,
                wavelet,
                num_crosslines,
                num_samples,
            )
            for _ in range(num_inlines)
        ]
    ).astype(np.float32)

    __save_seismic_to_segy(seismic_data, filepath, dt)

    return filepath


def __ricker_wavelet(frequency: int, length: int, dt: float) -> np.ndarray:
    t = np.linspace(-length / 2, (length / 2) - dt, length) * dt
    y = (1 - 2 * (np.pi**2) * (frequency**2) * (t**2)) * np.exp(
        -(np.pi**2) * (frequency**2) * (t**2)
    )

    return y


def __generate_synthetic_seismic(
    reflectivity: float,
    wavelet: np.ndarray,
    num_traces: int,
    num_samples: int,
) -> np.ndarray:
    seismic_data = np.zeros((num_traces, num_samples))
    for i in range(num_traces):
        seismic_data[i, :] = convolve(reflectivity, wavelet, mode="same")

    return seismic_data


def __save_seismic_to_segy(
    data: np.ndarray,
    filename: str,
    sample_interval: int,
) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    num_inlines, num_samples, num_crosslines = data.shape
    sample_interval_microseconds = int(sample_interval * 1e6)

    spec = segyio.spec()
    spec.sorting = 2
    spec.format = 1
    spec.samples = np.arange(num_samples) * sample_interval
    spec.ilines = np.arange(1, num_inlines + 1)
    spec.xlines = np.arange(1, num_crosslines + 1)
    spec.tracecount = num_inlines * num_crosslines

    with segyio.create(filename, spec) as segyfile:
        trace_index = 0
        for iline in spec.ilines:
            for xline in spec.xlines:
                segyfile.header[trace_index] = {
                    segyio.su.iline: iline,
                    segyio.su.xline: xline,
                }
                segyfile.trace[trace_index] = data[iline - 1, :, xline - 1].flatten()
                trace_index += 1

        segyfile.bin[segyio.BinField.Interval] = sample_interval_microseconds
        segyfile.bin[segyio.BinField.Traces] = spec.tracecount
        segyfile.bin[segyio.BinField.Samples] = num_samples
