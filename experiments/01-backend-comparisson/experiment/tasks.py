import random
import dowser


def consume_large_memory(num_elements: int) -> float:
    logger = dowser.get_logger()
    data = [random.random() for _ in range(num_elements)]

    logger.info(f"Consumed {num_elements} elements")

    return sum(data)


if __name__ == "__main__":
    consume_large_memory(10_000_000)
