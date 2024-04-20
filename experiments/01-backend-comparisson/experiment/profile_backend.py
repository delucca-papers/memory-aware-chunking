import os

from dowser import profile, config
from consume_large_memory import consume_large_memory


if __name__ == "__main__":
    experiment_backend_name = os.environ.get("EXPERIMENT_BACKEND")
    experiment_execution_id = os.environ.get("EXPERIMENT_EXECUTION_ID", None)
    experiment_num_elements = int(os.environ.get("EXPERIMENT_NUM_ELEMENTS", 1_000_000))
    experiment_output_dir = os.environ.get("EXPERIMENT_OUTPUT_DIR", "./output")
    experiment_unit = os.environ.get("EXPERIMENT_UNIT", "mb")
    experiment_logging_level = os.environ.get("EXPERIMENT_LOGGING_LEVEL", "DEBUG")

    input_metadata = f"num_elements={experiment_num_elements}"

    experiment_config = {
        "execution_id": experiment_execution_id,
        "output_dir": experiment_output_dir,
        "logging": {
            "level": experiment_logging_level,
        },
        "input": {
            "metadata": input_metadata,
        },
        "profiler": {
            "memory_usage": {
                "backend": experiment_backend_name,
                "report": {
                    "unit": experiment_unit,
                    "suffix": f"-{experiment_backend_name}",
                },
            },
        },
    }

    if not experiment_backend_name:
        raise ValueError(
            'You must provide a backend name on the "EXPERIMENT_BACKEND" environment variable'
        )

    config.update(experiment_config)
    profile(consume_large_memory)(experiment_num_elements)
