import os
import dowser

from seismic.data.synthetic import generate_and_save_synthetic_data


def generate_data(
    experiment_num_inlines: int,
    experiment_num_crosslines: int,
    experiment_num_samples: int,
) -> None:
    logger = dowser.get_logger()
    logger.info("Generating synthetic data for experiment")
    logger.debug(f"Number of inlines: {experiment_num_inlines}")
    logger.debug(f"Number of crosslines: {experiment_num_crosslines}")
    logger.debug(f"Number of samples: {experiment_num_samples}")

    output_dir = dowser.context.config.output_dir

    generate_and_save_synthetic_data(
        experiment_num_inlines,
        experiment_num_crosslines,
        experiment_num_samples,
        output_dir=output_dir,
    )

    logger.info(f"Finished generating synthetic data. Data stored on: {output_dir}")


if __name__ == "__main__":
    experiment_num_inlines = int(os.environ.get("EXPERIMENT_NUM_INLINES"))
    experiment_num_crosslines = int(os.environ.get("EXPERIMENT_NUM_CROSSLINES"))
    experiment_num_samples = int(os.environ.get("EXPERIMENT_NUM_SAMPLES"))
    experiment_output_dir = os.environ.get("EXPERIMENT_OUTPUT_DIR", "./output")
    experiment_logging_level = os.environ.get("EXPERIMENT_LOGGING_LEVEL", "DEBUG")
    experiment_logging_transports = os.environ.get(
        "EXPERIMENT_LOGGING_TRANSPORTS", "CONSOLE,FILE"
    ).split(",")

    dowser.load_config(
        {
            "output_dir": experiment_output_dir,
            "logger": {
                "enabled_transports": experiment_logging_transports,
                "level": experiment_logging_level,
            },
        }
    )

    generate_data(
        experiment_num_inlines,
        experiment_num_crosslines,
        experiment_num_samples,
    )
