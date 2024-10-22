import dask.array as da
import numpy as np
from datasets import load_segy
from scipy import ndimage as ndi

__all__ = [
    "gaussian_filter_from_segy",
    "gaussian_filter_from_ndarray",
    "gaussian_filter_from_dask_array",
]


def gaussian_filter_from_dask_array(dask_array: da.Array, sigma=(3, 3, 3)):
    result = dask_array.map_blocks(
        ndi.gaussian_filter, sigma=sigma, dtype=dask_array.dtype
    )

    return result.compute()


def gaussian_filter_from_ndarray(data: np.ndarray, sigma=(3, 3, 3)):
    dask_array = da.from_array(data, chunks="auto")
    return gaussian_filter_from_dask_array(dask_array, sigma)


def gaussian_filter_from_segy(segy_path: str, sigma=(3, 3, 3)):
    data = load_segy(segy_path)

    return gaussian_filter_from_ndarray(data, sigma)
