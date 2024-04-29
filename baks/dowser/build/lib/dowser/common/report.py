from abc import ABC, abstractmethod


class Report(ABC):
    @abstractmethod
    def add_log(self, metric: str, entries: list, metadata: dict) -> None:
        pass


__all__ = ["Report"]
