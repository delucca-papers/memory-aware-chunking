def align_tuples(tuples: list[tuple]) -> list[tuple]:
    max_length = max(len(first) for first, _ in tuples)

    formatted_tuples = []
    for first, second in tuples:
        padded_first = f"{first:{max_length}}\t"
        formatted_tuples.append((padded_first, second))

    return formatted_tuples


__all__ = ["align_tuples"]
