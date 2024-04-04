import logging

from multiprocessing import connection
from common.constants import FINISHED_EXPERIMENT, SUPERVISOR_RESPONSE
from common.profilers.proc import get_pid_status, get_peak_memory_usage_from_status


def watch_memory_usage(pid: str, conn: connection.Connection, output_dir: str) -> None:
    event = conn.recv()

    peak_memory_usage = __measure_memory(pid)
    logging.debug(
        f"Received event: {event} with peak memory usage: {peak_memory_usage}"
    )

    if event != FINISHED_EXPERIMENT:
        conn.send(SUPERVISOR_RESPONSE)
        watch_memory_usage(pid, conn, output_dir)


def __measure_memory(pid: str) -> int:
    logging.debug(f"Measuring memory usage for pid: {pid}")

    status = get_pid_status(pid)
    peak_memory = get_peak_memory_usage_from_status(status)

    return peak_memory
