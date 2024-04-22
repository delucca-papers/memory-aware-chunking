import os

from io import TextIOWrapper
from toolz import curry
from ..contexts import config

get_execution_id = config.lazy_get("execution_id")
get_output_dir = config.lazy_get("output_dir")


@curry
def go_to_pointer(pointer: int, file: TextIOWrapper) -> TextIOWrapper:
    file.seek(pointer)
    return file


@curry
def get_line_with_keyword(keyword: str, file: TextIOWrapper) -> str:
    for line in file:
        if keyword in line:
            return line

    return ""


@curry
def join_path(path: str, original: str) -> str:
    return os.path.join(original, path)


@curry
def add_ext(extension: str, filename: str) -> str:
    if extension not in filename:
        filename = f"{filename}.{extension}"

    return filename


def get_execution_output_dir() -> str:
    output_dir = get_output_dir()
    execution_id = get_execution_id()

    return join_path(execution_id, output_dir)


def to_absolute_output_path(relative_path: str) -> str:
    execution_output_dir = get_execution_output_dir()

    return join_path(relative_path, execution_output_dir)


__all__ = [
    "go_to_pointer",
    "get_line_with_keyword",
    "join_path",
    "add_ext",
    "get_execution_output_dir",
    "to_absolute_output_path",
]
