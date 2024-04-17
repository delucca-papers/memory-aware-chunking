from common.logging import get_module_logger

module_logger = get_module_logger()


def set_memory_limit_for_pid(cgroup_name: str, pid: int, memory_limit: int) -> None:
    module_logger.info(f"Setting memory limit for PID {pid} to {memory_limit} bytes")
    module_logger.debug(f"Using cgroup {cgroup_name}")

    with open(f"/sys/fs/cgroup/memory/{cgroup_name}/memory.limit_in_bytes", "w") as f:
        f.write(str(memory_limit))

    with open(f"/sys/fs/cgroup/memory/{cgroup_name}/cgroup.procs", "w") as f:
        f.write(str(pid))
