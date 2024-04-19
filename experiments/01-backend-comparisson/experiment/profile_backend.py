import os

from dowser import profile
from consume_large_memory import consume_large_memory


if __name__ == "__main__":
    num_elements = int(os.environ.get("EXPERIMENT_NUM_ELEMENTS", 1_000_000))
    backend_name = os.environ.get("EXPERIMENT_BACKEND")

    input_metadata = f"num_elements={num_elements}"
    experiment_config = {
        "input": {
            "metadata": input_metadata,
        },
        "profiler": {
            "memory_usage": {
                "backend": backend_name,
            },
        },
    }

    profile(
        consume_large_memory,
        config=experiment_config,
    )(num_elements)
