import os
import msgpack

from socket import socket
from typing import Callable
from dowser.common.logger import logger
from dowser.common.networking import receive_from_socket
from dowser.profiler.report import save_profile
from .constants import MESSAGE_LENGTH_BYTES


__all__ = ["consume_socket"]


def consume_socket(server: socket, socket_path: str, on_data: Callable) -> None:
    logger.info(f"Consuming socket on {socket_path}")

    try:
        connection, _ = server.accept()
        logger.debug("Got a new socket connection")

        while True:
            raw_length = receive_from_socket(connection, MESSAGE_LENGTH_BYTES)
            if not raw_length:
                break
            length = int.from_bytes(raw_length, "big")
            raw_data = receive_from_socket(connection, length)
            traces = msgpack.unpackb(raw_data)

            on_data(traces)
    finally:
        connection.close()
        server.close()
        os.unlink(socket_path)
