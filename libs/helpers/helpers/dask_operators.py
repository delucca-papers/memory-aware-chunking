import dask.array as da
import numpy as np
import segyio
from scipy import signal

__all__ = ["envelope_from_segy", "envelope_from_ndarray"]


def load_segy(segy_file_path: str) -> np.ndarray:
    with segyio.open(segy_file_path, "r", strict=False) as segyfile:
        return segyio.tools.cube(segyfile)


#### Envelope


def envelope_from_segy(segy_path: str):
    data = load_segy(segy_path)
    return envelope_from_ndarray(data)


def envelope_from_ndarray(data: np.ndarray):
    analytical_trace = da.map_blocks(signal.hilbert, data, dtype=data.dtype)
    absolute = da.absolute(analytical_trace)

    return absolute.compute()
