from typing import Any


def run(input: Any, n_workers: int = 1, single_threaded: bool = True):
    from dasf_seismic.attributes.texture import LocalBinaryPattern3D
    from ..cluster import run_attribute

    quality = LocalBinaryPattern3D()

    return run_attribute(quality, input, n_workers, single_threaded)
