import msgpack

from socket import socket
from typing import Optional, List
from dowser.common.networking import connect_socket
from dowser.profiler.types import (
    Trace,
    Source,
    Function,
    Event,
    CapturedTrace,
)
from .constants import MESSAGE_LENGTH_BYTES


__all__ = ["traces"]


class Traces:
    data: List[Trace] = []
    ignored_modules = ["dowser"]
    current_depth = 0
    socket_path: Optional[str] = None
    connection: Optional[socket] = None
    chunk_size: int = 10000

    def attach_socket(self, socket_path: str) -> None:
        self.socket_path = socket_path

    def connect_socket(self) -> None:
        self.connection = connect_socket(self.socket_path)

    def new_event(self, event: str) -> None:
        if event == "call":
            self.current_depth += 1
        elif event == "return":
            if self.current_depth > 0:
                self.current_depth -= 1

    def should_ignore(self, module_name: str) -> bool:
        module_name = module_name.split(".")[0]
        return module_name in self.ignored_modules

    def add_trace(
        self,
        source: Source,
        function: Function,
        event: Event,
        captured_traces: List[CapturedTrace],
    ) -> None:
        trace = {
            "source": source,
            "function": function,
            "event": event,
            **{key: value for key, value in captured_traces},
        }

        self.data.append(trace)
        if len(self.data) > self.chunk_size:
            self.flush()

    def flush(self) -> None:
        filtered_data = [
            trace for trace in self.data if not self.should_ignore(trace["source"])
        ]
        packed_traces = msgpack.packb(filtered_data)

        self.send_traces(packed_traces)
        self.data = []

    def send_traces(self, packed_traces: bytes) -> None:
        if not self.connection:
            self.connect_socket()

        self.connection.sendall(
            len(packed_traces).to_bytes(MESSAGE_LENGTH_BYTES, "big")
        )
        self.connection.sendall(packed_traces)


traces = Traces()
