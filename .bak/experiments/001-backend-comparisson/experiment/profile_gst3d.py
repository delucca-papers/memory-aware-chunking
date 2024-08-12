import os
import dowser

from seismic.attributes import gst_3d_dip


def run_experiment(experiment_data_dir: str) -> None:
    logger = dowser.get_logger()

    logger.info(
        f"Starting experiment with Session ID: {dowser.context.config.profiler.session_id}"
    )
    logger.debug(f"Experiment config: {dowser.context.config}")
    logger.debug(f"Data directory: {experiment_data_dir}")

    input_data_files = os.listdir(experiment_data_dir)
    input_data_segy_files = [
        file for file in input_data_files if file.endswith(".segy")
    ]
    input_data_filepath = os.path.join(experiment_data_dir, input_data_segy_files[0])
    logger.info(f"Input data file: {input_data_filepath}")

    dowser.profile(gst_3d_dip.run, input_data_filepath)


if __name__ == "__main__":
    experiment_backend_name = os.environ.get("EXPERIMENT_BACKEND_NAME")
    experiment_session_id = os.environ.get("EXPERIMENT_SESSION_ID", "experiment")
    experiment_output_dir = os.environ.get("EXPERIMENT_OUTPUT_DIR", "./output")
    experiment_data_dir = os.environ.get("EXPERIMENT_DATA_DIR", "./output/data")
    experiment_logging_level = os.environ.get("EXPERIMENT_LOGGING_LEVEL", "DEBUG")
    experiment_sign_traces = os.environ.get("EXPERIMENT_SIGN_TRACES", "false")
    experiment_logging_transports = os.environ.get(
        "EXPERIMENT_LOGGING_TRANSPORTS", "CONSOLE,FILE"
    ).split(",")

    if not experiment_backend_name:
        raise ValueError(
            'You must provide a backend name on the "EXPERIMENT_BACKEND_NAME" environment variable'
        )

    dowser.load_config(
        {
            "output_dir": experiment_output_dir,
            "logger": {
                "enabled_transports": experiment_logging_transports,
                "level": experiment_logging_level,
            },
            "profiler": {
                "session_id": experiment_session_id,
                "sign_traces": experiment_sign_traces,
                "memory_usage": {
                    "enabled_backends": [experiment_backend_name],
                },
            },
        }
    )

    run_experiment(experiment_data_dir)
