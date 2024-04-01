import random


def consume_large_memory(num_elements):
    large_list = [random.random() for _ in range(num_elements)]
    print(f"Created a list with {len(large_list)} elements")
