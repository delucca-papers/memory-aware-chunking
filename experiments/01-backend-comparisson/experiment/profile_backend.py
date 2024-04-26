import os

from dowser import profile
from dowser.logger import get_logger
from dowser.common import session_context
from dowser.profiler.context import profiler_context
from dowser.logger.context import logger_context
from tasks import consume_large_memory


def run_experiment(experiment_config: dict) -> None:
    logger_context.update(experiment_config.get("logger"))
    profiler_context.update(experiment_config.get("profiler"))
    session_context.update(experiment_config.get("session"))

    logger = get_logger()
    logger.info(f"Starting experiment with Session ID: {session_context.id}")
    logger.debug(f"Experiment config: {experiment_config}")

    profile(consume_large_memory)(experiment_num_elements)


if __name__ == "__main__":
    experiment_backend_name = os.environ.get("EXPERIMENT_BACKEND_NAME")
    experiment_session_id = os.environ.get("EXPERIMENT_SESSION_ID", "experiment")
    experiment_precision = int(os.environ.get("EXPERIMENT_PRECISION", "3"))
    experiment_num_elements = int(os.environ.get("EXPERIMENT_NUM_ELEMENTS", 1_000_000))
    experiment_output_dir = os.environ.get("EXPERIMENT_OUTPUT_DIR", "./output")
    experiment_unit = os.environ.get("EXPERIMENT_UNIT", "mb")
    experiment_logging_level = os.environ.get("EXPERIMENT_LOGGING_LEVEL", "DEBUG")

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
            },
        },
    }

    if not experiment_backend_name:
        raise ValueError(
            'You must provide a backend name on the "EXPERIMENT_BACKEND_NAME" environment variable'
        )

    run_experiment(experiment_config)
