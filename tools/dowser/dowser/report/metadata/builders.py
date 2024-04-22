from ...contexts import config
from ..transformers import align_tuples
from ..types import ReportMetadata


get_execution_id = config.lazy_get("execution_id")
get_input_metadata = config.lazy_get("report.metadata.input")


def build_extended_metadata(
    custom_metadata: ReportMetadata | None = None,
) -> ReportMetadata:
    metadata = build_default_metadata()
    if not custom_metadata:
        return metadata

    metadata.extend(custom_metadata)

    return metadata


def build_default_metadata() -> ReportMetadata:
    execution_id = get_execution_id()
    input_metadata = get_input_metadata()

    return [("Execution ID", execution_id), ("Input", input_metadata)]


def build_metadata_text(metadata: ReportMetadata) -> str:
    aligned_headers = align_tuples(metadata)

    return "\n".join([f"{first}: {second}" for first, second in aligned_headers])


__all__ = ["build_default_metadata", "build_metadata_text", "build_extended_metadata"]
