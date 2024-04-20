import os

from dowser import config
from dowser.core.logging import get_logger
from seismic.data.synthetic import generate_and_save_for_range


def generate_data(
    experiment_config: dict,
    experiment_num_inlines: int,
    experiment_num_crosslines: int,
    experiment_num_samples: int,
    experiment_step_size: int,
    experiment_range_size: int,
) -> None:
    config.update(experiment_config)
    execution_id = config.get("execution_id")
    output_dir = config.get("output_dir")

    logger = get_logger()
    logger.info(
        f"Generating synthetic data for experiment with Execution ID: {execution_id}"
    )

    data_dir = os.path.join(output_dir, execution_id, "data")

    generate_and_save_for_range(
        experiment_num_inlines,
        experiment_num_crosslines,
        experiment_num_samples,
        experiment_step_size,
        experiment_range_size,
        data_dir,
    )

    logger.info(f"Finished generating synthetic data. Data stored on: {data_dir}")


if __name__ == "__main__":
    experiment_execution_id = os.environ.get("EXPERIMENT_EXECUTION_ID")
    experiment_num_inlines = int(os.environ.get("EXPERIMENT_NUM_INLINES"))
    experiment_num_crosslines = int(os.environ.get("EXPERIMENT_NUM_CROSSLINES"))
    experiment_num_samples = int(os.environ.get("EXPERIMENT_NUM_SAMPLES"))
    experiment_step_size = int(os.environ.get("EXPERIMENT_STEP_SIZE"))
    experiment_range_size = int(os.environ.get("EXPERIMENT_RANGE_SIZE"))
    experiment_output_dir = os.environ.get("EXPERIMENT_OUTPUT_DIR", "./output")
    experiment_logging_level = os.environ.get("EXPERIMENT_LOGGING_LEVEL", "DEBUG")

    experiment_config = {
        "execution_id": experiment_execution_id,
        "output_dir": experiment_output_dir,
        "logging": {
            "level": experiment_logging_level,
        },
    }

    generate_data(
        experiment_config,
        experiment_num_inlines,
        experiment_num_crosslines,
        experiment_num_samples,
        experiment_step_size,
        experiment_range_size,
    )
