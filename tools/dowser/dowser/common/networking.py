import socket

from .logger import logger


__all__ = ["receive_from_socket", "start_socket", "connect_socket"]


def receive_from_socket(conn: socket.socket, length: int):
    data = b""
    while len(data) < length:
        more = conn.recv(length - len(data))
        if not more:
            return None
        data += more

    return data


def start_socket(socket_path: str) -> socket.socket:
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(socket_path)

    server.listen()
    logger.info(f"Socket server is listening on {socket_path}")

    return server


def connect_socket(socket_path: str) -> socket.socket:
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(socket_path)

    return client
