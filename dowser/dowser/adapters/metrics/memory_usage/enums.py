from enum import Enum


class MemoryUsageBackendName(Enum):
    PSUTIL = "psutil"
    RESOURCE = "resource"
    KERNEL = "kernel"
