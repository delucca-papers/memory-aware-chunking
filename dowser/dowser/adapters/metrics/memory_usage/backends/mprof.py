import io
import re

from typing import TypedDict
from memory_profiler import profile
from .base import MemoryUsageBackend


class MprofBackend(MemoryUsageBackend):
    pass


class UsedMemory(TypedDict):
    value: float
    unit: str


def run_profiled(fn: callable, *args, **kwargs) -> io.StringIO:
    stream = io.StringIO()

    profiled_function = profile(fn, stream=stream)
    profiled_function(*args, **kwargs)

    return stream


def get_initial_memory_usage_from_report(report: io.StringIO) -> UsedMemory:
    report_body = get_report_body(report)
    memory_usages = get_memory_usages_from_report_body(report_body)

    return memory_usages[0]


def get_peak_memory_usage_from_report(report: io.StringIO) -> UsedMemory:
    report_body = get_report_body(report)
    memory_usages = get_memory_usages_from_report_body(report_body)

    return max(memory_usages, key=lambda increment: increment["value"])


def get_final_memory_usage_from_report(report: io.StringIO) -> UsedMemory:
    report_body = get_report_body(report)
    memory_usages = get_memory_usages_from_report_body(report_body)

    return {
        "value": memory_usages[-1]["value"],
        "unit": memory_usages[-1]["unit"],
    }


def get_memory_usages_from_report_body(report_body: list[str]) -> list[UsedMemory]:
    increments = []
    for line in report_body:
        splitted_line = line.split()
        value = splitted_line[1]
        unit = splitted_line[2]

        increments.append({"value": float(value), "unit": unit})

    return increments


def get_report_body(report: io.StringIO) -> list[str]:
    report.seek(0)
    lines = report.readlines()
    return lines[4:-2]
