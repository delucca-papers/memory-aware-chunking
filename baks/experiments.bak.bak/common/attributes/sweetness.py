from typing import Any


def run(input: Any, n_workers: int = 1, single_threaded: bool = True):
    from dasf_seismic.attributes.complex_trace import Sweetness
    from common.cluster import run_attribute

    quality = Sweetness()

    return run_attribute(quality, input, n_workers, single_threaded)
