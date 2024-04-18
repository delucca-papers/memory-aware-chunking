import random

from dowser.logging import Logger

logger = Logger("ConsumeLargeMemory")


def consume_large_memory(num_elements):
    large_list = [random.random() for _ in range(num_elements)]
    logger.info(f"Created a list with {len(large_list)} elements")
