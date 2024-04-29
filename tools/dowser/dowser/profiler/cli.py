from argparse import _SubParsersAction
from uuid import uuid4
from dowser.common import AppendUnique
from .main import run_profiler


__all__ = ["attach_profiler_args"]


def attach_profiler_args(subparsers: _SubParsersAction) -> _SubParsersAction:
    profile_parser = subparsers.add_parser(
        "profile",
        help="Profile enabled metrics of a Python program",
    )

    profile_parser.add_argument(
        "--enabled-metrics",
        "-m",
        help="Metrics to use for the profiling session (default: memory_usage,time)",
        choices=["memory_usage", "time"],
        action="append",
    )

    profile_parser.add_argument(
        "--memory-usage-enabled-backends",
        "-b",
        help="Memory usage backends to use for the profiling session (default: psutil,resource,tracemalloc,mprof,kernel)",
        choices=["psutil", "resource", "tracemalloc", "mprof", "kernel"],
        action=AppendUnique,
    )

    profile_parser.add_argument(
        "--memory-usage-unit",
        help="Unit to use for the memory usage (default: mb)",
        choices=["kb", "mb", "gb"],
    )

    profile_parser.add_argument(
        "--session-id",
        help="Session ID to use for the profiling session (default: random UUID4)",
    )

    profile_parser.add_argument("script", help="Path to the Python script to execute")
    profile_parser.add_argument(
        "args",
        nargs="*",
        help="Arguments that will be passed to your script",
    )

    profile_parser.set_defaults(func=run_profiler)

    return subparsers
