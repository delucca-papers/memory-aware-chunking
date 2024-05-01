from typing import Callable, Literal
from toolz import curry
from .multiprocessing import parallelized_profiler as mp_parallelized_profiler
from .threading import parallelized_profiler as th_parallelized_profiler
from .synchronization import hook_sync_event


@curry
def build_parallelized_profiler(
    profiler: Callable,
    function: Callable,
    precision: float,
    *profiler_args,
    strategy: Literal["process", "thread"] = "process",
    **profiler_kwargs,
):
    available_handlers = {
        "process": mp_parallelized_profiler,
        "thread": th_parallelized_profiler,
    }
    parallelized_handler = available_handlers.get(strategy, mp_parallelized_profiler)

    get_result, sync_event = parallelized_handler(
        profiler,
        precision,
        *profiler_args,
        **profiler_kwargs,
    )

    hooked_function = hook_sync_event(function, sync_event)

    return hooked_function, get_result


__all__ = ["build_parallelized_profiler"]
