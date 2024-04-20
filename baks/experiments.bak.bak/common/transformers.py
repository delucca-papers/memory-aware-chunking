def bytes_to_mib(bytes_value: int):
    return bytes_value / (1024**2)


def kib_to_mib(kib_value: int):
    return kib_value / 1024


def dataset_path_to_name(dataset_path: str) -> str:
    return dataset_path.split("/")[-1].split(".")[0]
