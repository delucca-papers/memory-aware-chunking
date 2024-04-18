from enum import Enum


class MemoryUsageBackendName(Enum):
    PSUTIL = "psutil"
    RESOURCE = "resource"
    MPROF = "mprof"
    TRACEMALLOC = "tracemalloc"
    KERNEL = "kernel"
