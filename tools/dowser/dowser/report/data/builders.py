from ..transformers import align_tuples
from ..types import ReportData


def build_data_text(data: ReportData) -> str:
    aligned_data = align_tuples(data)

    return "\n".join(["\t".join([first, second]) for first, second in aligned_data])


__all__ = ["build_data_text"]
