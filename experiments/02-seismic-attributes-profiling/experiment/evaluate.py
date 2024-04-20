import os
import importlib

from dowser import config, collect_profile
from dowser.core.logging import get_logger
from seismic.data.loaders import load_segy


def run_experiment(experiment_config: dict, experiment_attributes: list[str]) -> None:
    config.update(experiment_config)
    logger = get_logger()

    execution_id = config.get("execution_id")
    output_dir = config.get("output_dir")
    experiment_data = os.path.join(output_dir, execution_id, "data")

    logger.info(f"Running experiment with Execution ID: {execution_id}")
    logger.debug(f"Experiment configuration: {experiment_config}")
    logger.debug(f"Experiment attributes: {experiment_attributes}")
    logger.debug(f"Data directory: {experiment_data}")

    inputs = __list_inputs(experiment_data)

    for attribute in experiment_attributes:
        logger.info(f"Starting experiment for attribute {attribute}")

        attribute_module = importlib.import_module(f"seismic.attributes.{attribute}")
        if not attribute_module or not hasattr(attribute_module, "run"):
            logger.error(f"Attribute {attribute} does not exist")
            continue

        collect_profile(
            attribute_module.run,
            inputs,
            input_handler=load_segy,
            group_name=attribute,
        )

        logger.info(f"Finished experiment with attribute {attribute}")

    logger.info("Finished executing experiment")


def __list_inputs(data_dir: str) -> list[str]:
    return [os.path.join(data_dir, filename) for filename in os.listdir(data_dir)]


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
        "model": {
            "collect": {
                "num_iterations": experiment_num_iterations,
            }
        },
    }

    run_experiment(experiment_config, experiment_attributes)
