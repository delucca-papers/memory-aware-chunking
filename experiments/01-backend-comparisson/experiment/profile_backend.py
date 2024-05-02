import os
import dowser

from tasks import consume_large_memory


def run_experiment(experiment_num_elements: int) -> None:
    logger = dowser.get_logger()

    logger.info(
        f"Starting experiment with Session ID: {dowser.context.config.profiler.session_id}"
    )
    logger.debug(f"Experiment config: {dowser.context.config}")

    dowser.profile(consume_large_memory, experiment_num_elements)


if __name__ == "__main__":
    experiment_backend_name = os.environ.get("EXPERIMENT_BACKEND_NAME")
    experiment_session_id = os.environ.get("EXPERIMENT_SESSION_ID", "experiment")
    experiment_num_elements = int(os.environ.get("EXPERIMENT_NUM_ELEMENTS", 1_000_000))
    experiment_output_dir = os.environ.get("EXPERIMENT_OUTPUT_DIR", "./output")
    experiment_logging_level = os.environ.get("EXPERIMENT_LOGGING_LEVEL", "DEBUG")
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
                "memory_usage": {
                    "enabled_backends": [experiment_backend_name],
                },
            },
        }
    )

    run_experiment(experiment_num_elements)
