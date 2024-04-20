import random
from dowser.core.logging import get_logger


def consume_large_memory(num_elements) -> float:
    logger = get_logger()
    data = [random.random() for _ in range(num_elements)]
    logger.info(f"Consumed {num_elements} elements")

    return sum(data)
