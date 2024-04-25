import os

from dowser.common import Context


class LoggerContext(Context):
    _base_path: str = "logger"
    _initial_data: dict = {
        "enabled_transports": "console,file",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "level": "info",
        "transports": {
            "file": {
                "filename": "dowser",
                "output_dir": "./",
                "max_bytes": "10485760",
                "backup_count": "3",
            }
        },
    }

    @property
    def enabled_transports(self) -> list[str]:
        return self.get("enabled_transports").split(",")

    @property
    def format(self) -> str:
        return self.get("format")

    @property
    def level(self) -> str:
        return self.get("level").upper()

    @property
    def transport_file_max_bytes(self) -> int:
        return int(self.get("transports.file.max_bytes"))

    @property
    def transport_file_backup_count(self) -> int:
        return int(self.get("transports.file.backup_count"))

    @property
    def transport_file_filename(self) -> str:
        return self.get("transports.file.filename")

    @property
    def transport_file_output_dir(self) -> str:
        return self.get("transports.file.output_dir")

    @property
    def transport_file_abspath(self) -> str:
        filename = self.transport_file_filename
        filename_with_ext = (
            f"{filename}.log" if not filename.endswith(".log") else filename
        )

        return os.path.join(self.transport_file_output_dir, filename_with_ext)


logger_context = LoggerContext()


__all__ = ["logger_context"]
