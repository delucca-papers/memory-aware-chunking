import os

from dowser import config
from dowser.core.logging import get_logger


def run_experiment(
    experiment_config: dict,
    experiment_num_iterations: int,
    experiment_attributes: list[str],
) -> None:
    config.update(experiment_config)
    logger = get_logger()

    execution_id = config.get("execution_id")
    output_dir = config.get("output_dir")
    experiment_data = os.path.join(output_dir, execution_id, "data")

    logger.info(f"Running experiment with Execution ID: {execution_id}")
    logger.debug(f"Experiment configuration: {experiment_config}")
    logger.debug(f"Experiment attributes: {experiment_attributes}")
    logger.debug(f"Number of iterations: {experiment_num_iterations}")
    logger.debug(f"Data directory: {experiment_data}")


if __name__ == "__main__":
    experiment_execution_id = os.environ.get("EXPERIMENT_EXECUTION_ID")
    experiment_output_dir = os.environ.get("EXPERIMENT_OUTPUT_DIR", "./output")
    experiment_logging_level = os.environ.get("EXPERIMENT_LOGGING_LEVEL", "DEBUG")
    experiment_num_iterations = int(os.environ.get("EXPERIMENT_NUM_ITERATIONS"))
    experiment_attributes = os.environ.get("EXPERIMENT_ATTRIBUTES").split(",")

    experiment_config = {
        "execution_id": experiment_execution_id,
        "output_dir": experiment_output_dir,
        "logging": {
            "level": experiment_logging_level,
        },
    }

    run_experiment(
        experiment_config,
        experiment_num_iterations,
        experiment_attributes,
    )
