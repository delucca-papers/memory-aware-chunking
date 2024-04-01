import resource


def get_current_memory_usage():
    return resource.getrusage(resource.RUSAGE_SELF)


def get_current_memory_usage_from_rusage(rusage):
    return rusage.ru_maxrss


def get_peak_memory_usage_from_rusage(rusage):
    """Resource does not provide a way to get peak memory usage."""
    return 0
