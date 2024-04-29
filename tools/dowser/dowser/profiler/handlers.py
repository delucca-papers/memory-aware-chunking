import sys

from pathlib import Path
from dowser.common.logger import logger


__all__ = ["execute_file"]


def execute_file(
    filepath: Path,
    args: tuple,
    kwargs: dict,
    function_name: str | None = None,
    before: callable = lambda: None,
    after: callable = lambda: None,
) -> None:
    logger.info(
        f'Starting new profiler session for file "{filepath}" with entrypoint set to: "{function_name if function_name else "__main__"}"'
    )
    logger.debug(f"Using args: {args}")
    logger.debug(f"Using kwargs: {kwargs}")

    original_argv = sys.argv.copy()
    sys.argv = [str(filepath)] + list(args)
    exec_globals = {
        "__name__": "__main__.sub" if function_name else "__main__",
        "__file__": str(filepath),
        "__package__": None,
        "__builtins__": __builtins__,
    }

    with open(filepath, "r") as f:
        file = f.read()

    try:
        before()
        exec(file, exec_globals)
        if function_name:
            function = exec_globals[function_name]
            function(*args, **kwargs)
        after()
    finally:
        sys.argv = original_argv
        logger.info(f'File "{filepath}" finished execution')
