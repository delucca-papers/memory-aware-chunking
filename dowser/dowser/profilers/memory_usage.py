import importlib

from typing import Callable, Any
from toolz import compose, curry
from toolz.curried import map
from functools import wraps
from ..core.transformers import convert_to, format_float
from ..core.config import config, get_namespace, get_config
from ..core.logging import get_logger
from ..core.report import build_report, save_report
from ..core.file_handling import join_path
from ..core.types import ReportLine
from .types import MemoryUsageLog, MemoryUsage

get_memory_usage_profiler_config = lambda c: get_namespace("profiler.memory_usage", c)
get_profiler_dir = lambda c: get_config("profiler.output_dir", c)

get_backend_name = lambda c: compose(
    lambda c: get_config("backend", c),
    get_memory_usage_profiler_config,
)(c)
get_precision = lambda c: compose(
    lambda p: 10**-p,
    lambda c: float(get_config("precision", c)),
    get_memory_usage_profiler_config,
)(c)

get_report_unit = lambda c: compose(
    lambda c: get_config("report.unit", c),
    get_memory_usage_profiler_config,
)(c)
get_report_filename = lambda c: compose(
    lambda c: get_config("report.filename", c),
    get_memory_usage_profiler_config,
)(c)
get_report_prefix = lambda c: compose(
    lambda c: get_config("report.prefix", c),
    get_memory_usage_profiler_config,
)(c)
get_report_suffix = lambda c: compose(
    lambda c: get_config("report.suffix", c),
    get_memory_usage_profiler_config,
)(c)
get_report_decimal_places = lambda c: compose(
    lambda c: int(get_config("report.decimal_places", c)),
    get_memory_usage_profiler_config,
)(c)
get_report_zfill = lambda c: compose(
    lambda c: int(get_config("report.zfill", c)),
    get_memory_usage_profiler_config,
)(c)
get_report_zfill_character = lambda c: compose(
    lambda c: get_config("report.zfill_character", c),
    get_memory_usage_profiler_config,
)(c)


###


def with_backend(function: Callable, config: dict = config) -> Any:
    logger = get_logger()
    backend_name = get_backend_name(config)
    precision = get_precision(config)
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
def report_memory_usage(
    function_name: str,
    profiler_results: MemoryUsageLog,
    config: dict = config,
) -> str:
    logger = get_logger()
    logger.debug(f"Building report for function {function_name}")

    precision = get_precision(config)
    backend = get_backend_name(config)

    custom_headers = [
        ("Backend", backend),
        ("Precision", f"{str(precision)} seconds"),
        ("Function", function_name),
    ]

    data = process_results(profiler_results, config=config)
    report = build_report(custom_headers, data, config=config)
    report_path = build_report_path(config=config)

    save_report(report, report_path, config=config)


def process_results(
    profiler_results: MemoryUsageLog,
    config: dict = config,
) -> list[ReportLine]:
    return compose(
        list,
        map(process_result_line(config)),
    )(profiler_results)


@curry
def process_result_line(config: dict, result: MemoryUsage) -> ReportLine:
    memory_usage, unit = result
    report_unit = get_report_unit(config)
    decimal_places = get_report_decimal_places(config)
    zfill = get_report_zfill(config)
    zfill_character = get_report_zfill_character(config)

    converted_memory_usage = convert_to(report_unit, unit, memory_usage)
    formatted_memory_usage = format_float(
        decimal_places,
        zfill,
        zfill_character,
        converted_memory_usage,
    )

    return "MEMORY_USAGE", f"{formatted_memory_usage} {report_unit.upper()}"


def build_report_path(config: dict = config) -> str:
    profiler_output_dir = get_profiler_dir(config)
    filename = get_report_filename(config)
    prefix = get_report_prefix(config)
    suffix = get_report_suffix(config)

    filename = f"{prefix}{filename}{suffix}"

    return join_path(filename, profiler_output_dir)


###


def profile(config: dict = config) -> Callable:
    logger = get_logger()
    def decorator(function: Callable) -> Callable:
        logger.info(
            f'Setting up memory usage profiler for function "{function.__name__}"'
        )

        profiled_function = with_backend(function, config=config)
        report_function_results = report_memory_usage(function.__name__, config=config)

        @wraps(profiled_function)
        def wrapper(*args, **kwargs) -> Any:
            profiler_results, function_results = profiled_function(*args, **kwargs)

            logger.debug(f"Profiler results: {profiler_results}")
            report_function_results(profiler_results)

            logger.info(f"Finished memory profiler for function {function.__name__}")

            return function_results

        return wrapper

    return decorator


__all__ = ["profile"]
