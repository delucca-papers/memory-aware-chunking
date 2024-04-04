import os
import random

from multiprocessing import Process, Pipe
from time import sleep
from common.profilers.proc import (
    get_pid_status,
    get_peak_memory_usage_from_status,
)


def task_process(conn):
    conn.send("NEW")

    response = conn.recv()

    large_list = [random.random() for _ in range(1_000_000)]
    print(f"Created a list with {len(large_list)} elements")

    conn.send("NEW")

    response = conn.recv()

    conn.close()


if __name__ == "__main__":
    print("ok")
    parent_conn, child_conn = Pipe()

    p = Process(target=task_process, args=(child_conn,))
    p.start()

    task_pid = p.pid
    self_pid = os.getpid()

    request = parent_conn.recv()

    print("Before")

    task_status = get_pid_status(task_pid)
    task_peak_memory = get_peak_memory_usage_from_status(task_status)
    print(f"Task peak memory: {task_peak_memory}")

    self_status = get_pid_status(self_pid)
    self_peak_memory = get_peak_memory_usage_from_status(self_status)
    print(f"Self peak memory: {self_peak_memory}")

    parent_conn.send("boo")

    request = parent_conn.recv()

    print("After")

    task_status = get_pid_status(task_pid)
    task_peak_memory = get_peak_memory_usage_from_status(task_status)
    print(f"Task peak memory: {task_peak_memory}")

    self_status = get_pid_status(self_pid)
    self_peak_memory = get_peak_memory_usage_from_status(self_status)
    print(f"Self peak memory: {self_peak_memory}")

    parent_conn.send("boo")

    p.join()
