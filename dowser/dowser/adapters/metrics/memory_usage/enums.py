from enum import Enum


class MemoryUsageBackendName(Enum):
    MPROF = "mprof"
    PSUTIL = "psutil"
    RESOURCE = "resource"
    KERNEL = "kernel"
