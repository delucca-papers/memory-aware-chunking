from typing import Any


def run(input: Any, n_workers: int = 1, single_threaded: bool = True):
    from dasf_seismic.attributes.dip_azm import GradientStructureTensor3DAzm
    from common.cluster import run_attribute

    quality = GradientStructureTensor3DAzm()

    return run_attribute(quality, input, n_workers, single_threaded)
