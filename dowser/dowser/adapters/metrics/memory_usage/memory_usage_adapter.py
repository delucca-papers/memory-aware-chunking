from typing import Callable, Any
from .backends import (
    KernelBackend,
    MprofBackend,
    PsutilBackend,
    ResourceBackend,
    MemoryUsageBackend,
)
from .enums import MemoryUsageBackendName
from ...logging import Logger
from ...config import ConfigManager


class MemoryUsageAdapter:
    __logger: Logger = Logger("MemoryUsageAdapter")
    __config: ConfigManager = ConfigManager()
    __backend: MemoryUsageBackend
    __available_backends: dict[MemoryUsageBackendName, type[MemoryUsageBackend]] = {
        MemoryUsageBackendName.KERNEL: KernelBackend,
        MemoryUsageBackendName.MPROF: MprofBackend,
        MemoryUsageBackendName.PSUTIL: PsutilBackend,
        MemoryUsageBackendName.RESOURCE: ResourceBackend,
    }

    @classmethod
    def from_backend_name(
        cls,
        backend_name: MemoryUsageBackendName | str | None,
    ) -> "MemoryUsageAdapter":
        backend_name = backend_name or cls.__config.get_config(
            "dowser.metrics.memory_usage.backend"
        )
        cls.__logger.debug(
            f'Creating memory usage adapter with backend: "{backend_name}"'
        )

        backend_name_enum = MemoryUsageBackendName(backend_name)
        Backend = cls.__available_backends.get(backend_name_enum)
        if Backend is None:
            raise ValueError(f"Unknown backend name: {backend_name}")

        return cls.from_backend(Backend)

    @classmethod
    def from_backend(cls, Backend: type[MemoryUsageBackend]) -> "MemoryUsageAdapter":
        backend = Backend()
        return cls(backend)

    def __init__(self, backend: MemoryUsageBackend):
        self.__backend = backend

    def profile(
        self,
        func: Callable,
        *func_args,
        **func_kwargs,
    ) -> Any:
        self.__logger.debug(f"Capturing memory usage for function: {func.__name__}")

        self.__backend.start_profiling(func.__name__)
        result = func(*func_args, **func_kwargs)
        self.__backend.stop_profiling()

        return result

    def update_backend_config(self, config: dict[str, Any]) -> "MemoryUsageAdapter":
        self.__backend.update_config(config)
        return self
