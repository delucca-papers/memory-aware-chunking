import importlib

from typing import Callable, Any
from toolz import compose, curry
from toolz.curried import map
from functools import wraps
from ..core import (
    convert_to,
    format_float,
    get_logger,
    join_path,
    full_function_name,
)
from ..report import save_report, ReportData, ReportRow
from ..contexts import config
from .types import MemoryUsageLog, MemoryUsage

get_profiler_dir = config.lazy_get("profiler.output_dir")
get_backend_name = config.lazy_get("profiler.memory_usage.backend")
get_report_unit = config.lazy_get("profiler.memory_usage.report.unit")
get_report_filename = config.lazy_get("profiler.memory_usage.report.filename")
get_report_prefix = config.lazy_get("profiler.memory_usage.report.prefix")
get_report_suffix = config.lazy_get("profiler.memory_usage.report.suffix")
get_report_decimal_places = config.lazy_get(
    "profiler.memory_usage.report.decimal_places",
    type=int,
)
get_report_zfill = config.lazy_get(
    "profiler.memory_usage.report.zfill",
    type=int,
)
get_report_zfill_character = config.lazy_get(
    "profiler.memory_usage.report.zfill_character"
)
get_precision = compose(
    lambda p: 10**-p,
    config.lazy_get("profiler.memory_usage.precision", type=float),
)


###


def with_backend(function: Callable) -> Any:
    logger = get_logger()
    backend_name = get_backend_name()
    precision = get_precision()
    logger.debug(f'Executing message usage profiler with "{backend_name}" backend')

    backend_module = importlib.import_module(
        f".backends.{backend_name}",
        package=__package__,
    )
    if backend_module is None:
        logger.error(f'Backend "{backend_name}" is not implemented yet')
        return

    backend_wrapper = getattr(backend_module, "wrapper")

    return backend_wrapper(function, precision)


@curry
def report_memory_usage(function: Callable, profiler_results: MemoryUsageLog) -> str:
    logger = get_logger()
    function_name = full_function_name(function)
    logger.debug(f"Building report for function {function_name}")

    precision = get_precision()
    backend = get_backend_name()

    custom_metadata = [
        ("Backend", backend),
        ("Precision", f"{str(precision)} seconds"),
        ("Function", function_name),
    ]

    data = process_results(profiler_results)
    report_path = build_report_path()

    save_report(data, report_path, custom_metadata=custom_metadata)


def process_results(profiler_results: MemoryUsageLog) -> ReportData:
    return compose(
        list,
        map(process_result_line),
    )(profiler_results)


@curry
def process_result_line(result: MemoryUsage) -> ReportRow:
    memory_usage, unit = result
    report_unit = get_report_unit()
    decimal_places = get_report_decimal_places()
    zfill = get_report_zfill()
    zfill_character = get_report_zfill_character()

    converted_memory_usage = convert_to(report_unit, unit, memory_usage)
    formatted_memory_usage = format_float(
        decimal_places,
        zfill,
        zfill_character,
        converted_memory_usage,
    )

    return "MEMORY_USAGE", f"{formatted_memory_usage} {report_unit.upper()}"


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
    logger.info(f'Setting up memory usage profiler for function "{function.__name__}"')

    profiled_function = with_backend(function)
    report_function_results = report_memory_usage(function)

    @wraps(profiled_function)
    def wrapper(*args, **kwargs) -> Any:
        profiler_results, function_results = profiled_function(*args, **kwargs)

        logger.debug(f"Profiler results: {profiler_results}")
        report_function_results(profiler_results)

        logger.info(f"Finished memory usage profiler for function {function.__name__}")

        return function_results

    return wrapper


__all__ = ["profile"]
