from dowser.common.logger import logger
from dowser.config import Config
from .loaders import load_session
from .builders import build_trace_tree


__all__ = ["compare_profiles"]


def compare_profiles(config: Config) -> None:
    logger.info("Starting profiles comparison")
    logger.debug(f"Using config: {config}")

    loaded_sessions = {
        name: load_session(path) for name, path in config.analyzer.sessions.items()
    }

    trace_tree = build_trace_tree(loaded_sessions["psutil"])
