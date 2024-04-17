import logging
import os

from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from ..config import ConfigManager


class Logger:
    __logger: logging.Logger
    __config: ConfigManager = ConfigManager()
    __formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    def __init__(
        self,
        name: str,
        output_dir: str | None = None,
        logfile: str | None = None,
        level: str | None = None,
    ):
        output_dir = output_dir or self.__config.get_config("dowser.output_dir")
        logfile = logfile or self.__config.get_config("dowser.logging.filename")
        level = level or self.__config.get_config("dowser.logging.level").upper()

        self.__logger = logging.getLogger(name)

        self.set_level(level)
        self.__setup_transports(logfile, output_dir)

    def debug(self, message: str) -> None:
        self.__logger.debug(message)

    def info(self, message: str) -> None:
        self.__logger.info(message)

    def warn(self, message: str) -> None:
        self.__logger.warn(message)

    def error(self, message: str) -> None:
        self.__logger.error(message)

    def critical(self, message: str) -> None:
        self.__logger.critical(message)

    def set_level(self, level: str) -> None:
        self.__logger.setLevel(level)

    def __setup_transports(self, logfile: str, output_dir: str) -> None:
        self.__setup_file_transport(logfile, output_dir)
        self.__setup_console_transport()

    def __setup_file_transport(self, logfile: str, output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)
        logfile_path = os.path.join(output_dir, logfile)
        file_handler = RotatingFileHandler(
            logfile_path,
            maxBytes=10485760,
            backupCount=3,
        )
        file_handler.setFormatter(self.__formatter)

        self.__logger.addHandler(file_handler)

    def __setup_console_transport(self) -> None:
        console_handler = StreamHandler()
        console_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(console_handler)
