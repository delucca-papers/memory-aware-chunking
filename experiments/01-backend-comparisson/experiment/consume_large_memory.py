import random


def consume_large_memory(num_elements) -> float:
    data = [random.random() for _ in range(num_elements)]
    return sum(data)
