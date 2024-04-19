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


@curry
def add_prefix_to_file_in_path(suffix: str, filepath: str) -> str:
    filepath_parts = filepath.split("/")
    filename = filepath_parts[-1]
    directory = "/".join(filepath_parts[:-1])

    filename = f"{suffix}-{filename}"

    return join_path(filename, directory)


__all__ = [
    "go_to_pointer",
    "get_line_with_keyword",
    "join_path",
    "add_ext",
    "add_prefix_to_file_in_path",
]
