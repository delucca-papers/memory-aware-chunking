import time

from typing import Tuple, Callable
from multiprocessing import Process, Manager
from dowser.common.logger import logger
from dowser.common.synchronization import run_subprocess, do_many
from dowser.profiler.types import TraceHooks
from dowser.profiler.buffer import Buffer

__all__ = ["create_samplers"]


def create_samplers(
    buffer: Buffer,
    trace_hooks: TraceHooks,
    precision: float,
    source: str = "UNKNOWN:0",
    function: str = "UNKNOWN",
) -> Tuple[Callable, Callable]:
    logger.info("Creating samplers")
    process: Process = None
    manager = Manager()
    should_terminate = manager.Value("b", False)

    def start_sampler() -> None:
        logger.debug("Starting sampler")

        nonlocal process
        do_many(trace_hooks.get("before", []))

        process = run_subprocess(
            sampler_loop,
            buffer,
            trace_hooks,
            precision,
            source,
            function,
            should_terminate,
        )

        logger.debug(f"Sampler started with PID: {process.pid}")

    def stop_sampler() -> None:
        logger.debug("Stopping sampler")

        do_many(trace_hooks.get("after", []))

        if process and process.is_alive():
            should_terminate.value = True
            process.join()
            logger.debug("Sampler stopped")

    return start_sampler, stop_sampler


def sampler_loop(
    buffer: Buffer,
    trace_hooks: TraceHooks,
    interval: float,
    source: str,
    function: str,
    should_terminate: bool,
) -> None:
    while not should_terminate.value:
        sample(buffer, trace_hooks, source, function)
        time.sleep(interval)

    buffer.flush()


def sample(buffer: Buffer, trace_hooks: TraceHooks, source: str, function: str) -> None:
    captured_traces = do_many(trace_hooks.get("on_sample", []))
    buffer.append(source, function, "sample", captured_traces)
