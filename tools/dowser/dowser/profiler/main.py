from dowser.common import Config, logger


__all__ = ["run_profiler"]


def run_profiler(config: Config) -> None:
    script_path = config.get("profiler.script")
    args = config.get("profiler.args")

    logger.info(f'Starting new profiler session for script "{script_path}"')
    logger.debug(f"Using args: {args}")
