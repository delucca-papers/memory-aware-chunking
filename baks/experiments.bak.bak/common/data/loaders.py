import segyio
import numpy as np

from ..logging import get_module_logger

module_logger = get_module_logger()


def load_segy(segy_file_path: str) -> np.ndarray[float]:
    module_logger.debug(f"Loading segy file: {segy_file_path}")

    with segyio.open(segy_file_path, "r", strict=False) as segyfile:
        return segyio.tools.cube(segyfile)
