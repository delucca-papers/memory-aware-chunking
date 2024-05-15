from dowser.config import Config
from dowser.common.logger import logger
from dowser.common.synchronization import run_subprocess
from .handlers import execute_file
from .report import save_profile
from .builders import (
    build_trace_hooks,
    build_executor_hooks,
    build_metadata,
)


__all__ = ["run_profiler"]


def run_profiler(config: Config) -> None:
    logger.info("Starting profiler")

    metadata = build_metadata(
        config.profiler.signature,
        config.profiler.args,
        config.profiler.kwargs,
    )
    trace_hooks = build_trace_hooks(
        config.profiler.enabled_metrics,
        config.profiler.memory_usage.enabled_backends,
    )
    on_trace_data = save_profile(
        config.output_dir,
        config.profiler.session_id,
        metadata,
    )
    executor_hooks = build_executor_hooks(
        trace_hooks,
        instrumentation_config=config.profiler.instrumentation,
        on_data=on_trace_data,
    )

    target_args = (
        config.profiler.filepath,
        config.profiler.args,
        config.profiler.kwargs,
    )
    target_kwargs = {"function_name": config.profiler.entrypoint, **executor_hooks}

    logger.debug(f"Using config: {config}")
    logger.debug(f"Using metadata: {metadata}")
    logger.debug(f"Enabled trace hooks: {trace_hooks.keys()}")
    logger.debug(f"Enabled metrics: {config.profiler.enabled_metrics}")
    logger.debug(f"Using args: {config.profiler.args}")
    logger.debug(f"Using kwargs: {config.profiler.kwargs}")

    logger.info(f'Starting profiler execution for "{config.profiler.filepath}"')

    run_subprocess(execute_file, sync=True, *target_args, **target_kwargs)

    logger.info("Profiler execution finished")
