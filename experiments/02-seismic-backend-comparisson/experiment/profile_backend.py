import os
import importlib
import sys

from dowser import profile
from dowser.common import session_context
from dowser.logger import get_logger
from dowser.logger.context import logger_context
from dowser.profiler.context import profiler_context


def run_experiment(
    experiment_config: dict,
    experiment_attribute: str,
    experiment_data_dir: str,
) -> None:
    session_context.update(experiment_config.get("session", {}))
    logger_context.update(experiment_config.get("logger", {}))
    profiler_context.update(experiment_config.get("profiler", {}))

    logger = get_logger()
    logger.info(f"Running experiment with Session ID: {session_context.id}")

    logger.debug(f"Experiment configuration: {experiment_config}")
    logger.debug(f"Experiment attribute: {experiment_attribute}")
    logger.debug(f"Data directory: {experiment_data_dir}")

    input_data_filename = os.listdir(experiment_data_dir)[0]
    input_data_filepath = os.path.join(experiment_data_dir, input_data_filename)

    attribute_module = importlib.import_module(
        f"seismic.attributes.{experiment_attribute}"
    )
    if not attribute_module or not hasattr(attribute_module, "run"):
        logger.error(f'Attribute "{experiment_attribute}" does not exist')
        sys.exit(1)

    profile(attribute_module.run)(input_data_filepath)

    logger.info("Finished executing experiment")


if __name__ == "__main__":
    experiment_backend_name = os.environ.get("EXPERIMENT_BACKEND_NAME")
    experiment_session_id = os.environ.get("EXPERIMENT_SESSION_ID", "experiment")
    experiment_output_dir = os.environ.get("EXPERIMENT_OUTPUT_DIR", "./output")
    experiment_data_dir = os.environ.get("EXPERIMENT_DATA_DIR", "./output/data")
    experiment_logging_level = os.environ.get("EXPERIMENT_LOGGING_LEVEL", "DEBUG")
    experiment_precision = int(os.environ.get("EXPERIMENT_PRECISION"))
    experiment_attribute = os.environ.get("EXPERIMENT_ATTRIBUTE")

    experiment_config = {
        "session": {
            "id": experiment_session_id,
            "output_dir": experiment_output_dir,
        },
        "logger": {
            "level": experiment_logging_level,
        },
        "profiler": {
            "metrics": {
                "memory_usage": {
                    "enabled_backends": experiment_backend_name,
                    "precision": experiment_precision,
                }
            }
        },
    }

    if not experiment_backend_name:
        raise ValueError(
            'You must provide a backend name on the "EXPERIMENT_BACKEND_NAME" environment variable'
        )

    if not experiment_attribute:
        raise ValueError(
            'You must provide an attribute name on the "EXPERIMENT_ATTRIBUTE" environment variable'
        )

    run_experiment(experiment_config, experiment_attribute, experiment_data_dir)
