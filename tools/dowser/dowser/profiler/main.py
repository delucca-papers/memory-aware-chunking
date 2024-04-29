from dowser.config import Config
from dowser.common.logger import logger


__all__ = ["run_profiler"]


def run_profiler(config: Config) -> None:
    script_path = config.profiler.script
    args = config.profiler.args

    logger.info(f'Starting new profiler session for script "{script_path}"')
    logger.debug(f"Using args: {args}")
