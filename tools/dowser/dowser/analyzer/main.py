from dowser.common.logger import logger
from dowser.config import Config
from .loaders import load_session


__all__ = ["compare_profiles"]


def compare_profiles(config: Config) -> None:
    logger.info("Starting profiles comparison")
    logger.debug(f"Using config: {config}")

    loaded_sessions = {
        name: load_session(path) for name, path in config.analyzer.sessions.items()
    }
