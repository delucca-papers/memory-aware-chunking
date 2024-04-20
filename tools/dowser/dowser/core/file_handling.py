import os

from io import TextIOWrapper
from toolz import curry


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


__all__ = [
    "go_to_pointer",
    "get_line_with_keyword",
    "join_path",
    "add_ext",
]
