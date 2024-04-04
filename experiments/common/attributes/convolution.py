from typing import Any


def run(input: Any, n_workers: int = 1, single_threaded: bool = True):
    from dasf_seismic.attributes.noise_reduction import Convolution
    from common.cluster import run_attribute

    quality = Convolution()

    return run_attribute(quality, input, n_workers, single_threaded)
