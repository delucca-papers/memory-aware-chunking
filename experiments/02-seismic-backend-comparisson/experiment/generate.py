import os

from dowser.common import session_context
from dowser.logger import get_logger
from dowser.logger.context import logger_context
from seismic.data.synthetic import generate_and_save_synthetic_data


def generate_data(
    experiment_config: dict,
    experiment_num_inlines: int,
    experiment_num_crosslines: int,
    experiment_num_samples: int,
) -> None:
    session_context.update(experiment_config.get("session", {}))
    logger_context.update(experiment_config.get("logger", {}))

    logger = get_logger()
    logger.info(
        f"Generating synthetic data for experiment with Session ID: {session_context.id}"
    )

    data_dir = os.path.join(session_context.output_dir, "data")

    generate_and_save_synthetic_data(
        experiment_num_inlines,
        experiment_num_crosslines,
        experiment_num_samples,
        output_dir=data_dir,
    )

    logger.info(f"Finished generating synthetic data. Data stored on: {data_dir}")


if __name__ == "__main__":
    experiment_session_id = os.environ.get("EXPERIMENT_SESSION_ID", "experiment")
    experiment_num_inlines = int(os.environ.get("EXPERIMENT_NUM_INLINES"))
    experiment_num_crosslines = int(os.environ.get("EXPERIMENT_NUM_CROSSLINES"))
    experiment_num_samples = int(os.environ.get("EXPERIMENT_NUM_SAMPLES"))
    experiment_output_dir = os.environ.get("EXPERIMENT_OUTPUT_DIR", "./output")
    experiment_logging_level = os.environ.get("EXPERIMENT_LOGGING_LEVEL", "DEBUG")

    experiment_config = {
        "session": {
            "id": experiment_session_id,
            "output_dir": experiment_output_dir,
        },
        "logger": {
            "level": experiment_logging_level,
        },
    }

    generate_data(
        experiment_config,
        experiment_num_inlines,
        experiment_num_crosslines,
        experiment_num_samples,
    )
