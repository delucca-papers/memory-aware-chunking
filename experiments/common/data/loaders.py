import segyio
import logging
import numpy as np


def load_segy(segy_file_path: str) -> np.ndarray[float]:
    logging.debug(f"Loading segy file: {segy_file_path}")

    with segyio.open(segy_file_path, "r", strict=False) as segyfile:
        data = segyio.tools.cube(segyfile)
        return data
