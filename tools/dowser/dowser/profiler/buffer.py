import re
import msgpack

from tempfile import TemporaryDirectory
from typing import List
from .types import TraceList, Source, Function, Event, CapturedTrace


__all__ = ["Buffer"]


class Buffer:
    data: TraceList = []
    current_depth = 0
    buffer_size: int = 100000
    buffered_files: int = 0
    temp_dir: TemporaryDirectory = TemporaryDirectory()
    ignore_pattern = re.compile(r"^(dowser)")

    def append(
        self,
        source: Source,
        function: Function,
        event: Event,
        captured_traces: List[CapturedTrace],
    ) -> None:
        if self.should_ignore(source):
            return

        data = {
            "source": source,
            "function": function,
            "event": event,
            **{key: value for key, value in captured_traces},
        }

        self.data.append(data)
        if len(self.data) > self.buffer_size:
            self.flush()

    def new_event(self, event: str) -> None:
        if event == "call":
            self.current_depth += 1
        elif event == "return":
            self.current_depth -= 1

    def should_ignore(self, module_name: str) -> bool:
        return self.ignore_pattern.match(module_name) is not None

    def flush(self) -> None:
        self.buffer_traces()
        self.data = []

    def buffer_traces(self) -> None:
        self.buffered_files += 1

        packed_traces = msgpack.packb(self.data)

        buffer_file_path = (
            f"{self.temp_dir.name}/buffer_{self.buffered_files:05d}.msgpack"
        )
        with open(buffer_file_path, "wb") as buffer_file:
            buffer_file.write(packed_traces)
