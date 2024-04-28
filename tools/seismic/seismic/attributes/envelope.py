def run(input: str, n_workers: int = 1, single_threaded: bool = True):
    from dasf_seismic.attributes.complex_trace import Envelope
    from ..cluster import run_attribute
    from ..data.loaders import load_segy

    input = load_segy(input)
    quality = Envelope()

    return run_attribute(quality, input, n_workers, single_threaded)
