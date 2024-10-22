import logging


__all__ = ["get_named_logger"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)


def get_named_logger(name: str):
    return logging.getLogger(name)
