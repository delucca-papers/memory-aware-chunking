import os
import msgpack
import gzip

from .types import Profile


__all__ = ["load_buffer", "load_profile"]


def load_buffer(temp_dir: str) -> list:
    buffer = []

    msgpack_files = sorted(f for f in os.listdir(temp_dir) if f.endswith(".msgpack"))

    for filename in msgpack_files:
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, "rb") as file:
            unpacker = msgpack.Unpacker(file, raw=False)
            for unpacked in unpacker:
                buffer.extend(unpacked)

    return buffer


def load_profile(filepath: str) -> Profile:
    with gzip.GzipFile(filepath, mode="rb") as gzip_file:
        return msgpack.unpackb(gzip_file.read(), raw=False)
