from enum import Enum


class MemoryUsageBackendName(Enum):
    PSUTIL = "psutil"
    RESOURCE = "resource"
    MPROF = "mprof"
    KERNEL = "kernel"
