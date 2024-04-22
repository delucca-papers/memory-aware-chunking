from ..core.transformers import deep_merge
from .base import Context


class ReportContext(Context):
    _data: dict = {
        "group": None,
    }

    def __init__(self, data: dict = {}):
        self._data = deep_merge(self._data, data)


report_context = ReportContext()

__all__ = ["report_context"]
