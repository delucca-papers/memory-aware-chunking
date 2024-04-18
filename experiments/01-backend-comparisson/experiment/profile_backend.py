import os

from dowser import profile
from dowser.logging import Logger
from consume_large_memory import consume_large_memory


if __name__ == "__main__":
    num_elements = int(os.environ.get("EXPERIMENT_NUM_ELEMENTS", 1_000_000))
    backend_name = os.environ.get("EXPERIMENT_BACKEND")

    logger = Logger(f"{backend_name.capitalize()}Psutil")
    logger.info(f"Starting {backend_name} backend experiment")

    input_metadata = f"num_elements={num_elements}"

    logger.info(f"Running experiment with {num_elements} elements")
    profile(
        consume_large_memory,
        input_metadata=input_metadata,
        memory_usage_backend=backend_name,
    )(num_elements)
