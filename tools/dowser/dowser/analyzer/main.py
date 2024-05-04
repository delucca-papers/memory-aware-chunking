from toolz import compose
from dowser.common.logger import logger
from dowser.config import Config
from .loaders import load_session
from .transformers import (
    explode_additional_data,
    column_to_unit,
    to_memory_usage_evolution,
)
from .plotters import plot_memory_usage_comparison, plot_execution_time_comparison


__all__ = ["compare_profiles"]


def compare_profiles(config: Config) -> None:
    logger.info("Starting profiles comparison")
    logger.debug(f"Using config: {config}")

    parse_profile = compose(
        column_to_unit("MEMORY_USAGE", config.analyzer.unit.value),
        explode_additional_data,
        load_session,
    )

    logger.info("Parsing collected profiles")
    collected_profiles = {
        name: parse_profile(path) for name, path in config.analyzer.sessions.items()
    }

    logger.debug("Parsing memory usage evolution data")

    memory_usage_evolution = {
        name: to_memory_usage_evolution(profile)
        for name, profile in collected_profiles.items()
    }

    plot_memory_usage_comparison(memory_usage_evolution, config.output_dir)
    plot_execution_time_comparison(memory_usage_evolution, config.output_dir)

    logger.info(f"Finished profiles comparison. Results saved to {config.output_dir}")
