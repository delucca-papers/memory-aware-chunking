def get_self_status():
    with open("/proc/self/status", "r") as status_file:
        return status_file.read()


def get_peak_memory_usage_from_status(status: str):
    line_list = status.split("\n")
    for line in line_list:
        if "VmPeak" in line:
            return int(line.split()[1])


def get_current_memory_usage_from_status(status: str):
    line_list = status.split("\n")
    for line in line_list:
        if "VmSize" in line:
            return int(line.split()[1])
