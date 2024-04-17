from psutil import Process
from typing import NamedTuple
from .base import MemoryUsageBackend


class PsutilBackend(MemoryUsageBackend):
    pass


def get_self_memory_info():
    process = Process()
    return process.memory_info()


def get_current_memory_usage_from_pmem(pmem: NamedTuple) -> int:
    return pmem.rss


def get_peak_memory_usage_from_pmem(_pmem: NamedTuple) -> int:
    """PSUtil does not provide a way to get peak memory usage."""
    return 0
