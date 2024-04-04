import numpy as np
import segyio
import os
import logging

from scipy.signal import convolve


def generate_and_save_for_range(
    num_inlines_step: int,
    num_inlines_range_size: int,
    num_crosslines: int,
    num_samples: int,
    output_dir: str,
) -> list[str]:
    logging.info(f"Generating synthetic data for range: {num_inlines_range_size}")
    logging.info(f"Using num_inlines step of {num_inlines_step}")

    return [
        generate_and_save_synthetic_data(
            step_num * num_inlines_step,
            num_crosslines,
            num_samples,
            output_dir=output_dir,
            filename=f"{step_num*num_inlines_step}-{num_crosslines}-{num_samples}.segy",
        )
        for step_num in range(1, num_inlines_range_size + 1)
    ]


def generate_and_save_synthetic_data(
    num_inlines: int,
    num_crosslines: int = 200,
    num_samples: int = 200,
    dt: float = 0.004,
    frequency: int = 25,
    length: int = 250,
    output_dir: str = "/tmp/synthetic_seismic_data",
    filename: str = "synthetic_seismic.segy",
) -> str:
    logging.debug(f"Generating synthetic data for {num_inlines} inlines")

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

    filepath = os.path.join(output_dir, filename)
    __save_seismic_to_segy(seismic_data, filepath, dt)

    return filepath


def __ricker_wavelet(frequency: int, length: int, dt: float) -> np.ndarray[float]:
    t = np.linspace(-length / 2, (length / 2) - dt, length) * dt
    y = (1 - 2 * (np.pi**2) * (frequency**2) * (t**2)) * np.exp(
        -(np.pi**2) * (frequency**2) * (t**2)
    )

    return y


def __generate_synthetic_seismic(
    reflectivity: float,
    wavelet: np.ndarray[float],
    num_traces: int,
    num_samples: int,
) -> np.ndarray[float]:
    seismic_data = np.zeros((num_traces, num_samples))
    for i in range(num_traces):
        seismic_data[i, :] = convolve(reflectivity, wavelet, mode="same")

    return seismic_data


def __save_seismic_to_segy(
    data: np.ndarray[float],
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
