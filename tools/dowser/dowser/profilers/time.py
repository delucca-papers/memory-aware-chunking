import time

from typing import Callable, Any
from functools import wraps
from toolz import curry, compose
from toolz.curried import map
from ..core import (
    get_logger,
    build_report,
    save_report,
    join_path,
    align_tuples,
    ReportLine,
)
from ..contexts import config
from .types import TimeLog, Time

get_profiler_dir = config.lazy_get("profiler.output_dir")
get_report_filename = config.lazy_get("profiler.time.report.filename")
get_report_prefix = config.lazy_get("profiler.time.report.prefix")
get_report_suffix = config.lazy_get("profiler.time.report.suffix")


###


@curry
def report_time(function_name: str, time_log: TimeLog) -> str:
    logger = get_logger()
    logger.debug(f"Building report for function {function_name}")

    custom_headers = [
        ("Function", function_name),
    ]

    data = process_results(time_log)
    report = build_report(custom_headers, data)
    report_path = build_report_path()

    save_report(report, report_path)


def process_results(time_log: TimeLog) -> list[ReportLine]:
    return compose(
        list,
        map(process_result_line),
    )(time_log)


@curry
def process_result_line(result: Time) -> ReportLine:
    unit = "SECONDS"
    event, time = result

    return event.upper(), f"{time} {unit}"


def build_report_path() -> str:
    profiler_output_dir = get_profiler_dir()
    filename = get_report_filename()
    prefix = get_report_prefix()
    suffix = get_report_suffix()

    filename = f"{prefix}{filename}{suffix}"

    return join_path(filename, profiler_output_dir)


###


def profile(function: Callable) -> Callable:
    logger = get_logger()
    logger.info(
        f'Setting up execution time profiler for function "{function.__name__}"'
    )

    report_function_results = report_time(function.__name__)

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        function_results = function(*args, **kwargs)
        end_time = time.time()

        profiler_results = [
            ("START", start_time),
            ("END", end_time),
            ("EXECUTION_TIME", end_time - start_time),
        ]

        logger.debug(f"Profiler results: {profiler_results}")
        report_function_results(profiler_results)

        logger.info(f"Finished time profiler for function {function.__name__}")

        return function_results

    return wrapper


__all__ = ["profile"]
