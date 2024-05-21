from dowser.config import Config
from dowser.common.logger import logger
from dowser.common.synchronization import run_subprocess
from .handlers import execute_file
from .buffer import Buffer
from .builders import (
    build_trace_hooks,
    build_executor_hooks,
    build_profile,
    build_metadata,
)


__all__ = ["run_profiler"]


def run_profiler(config: Config) -> None:
    logger.info("Starting profiler")

    buffer = Buffer()
    trace_hooks = build_trace_hooks(
        config.profiler.enabled_metrics,
        config.profiler.memory_usage.enabled_backends,
    )
    executor_hooks = build_executor_hooks(
        trace_hooks,
        buffer,
        strategy=config.profiler.strategy,
        instrumentation_config=config.profiler.instrumentation,
        sampling_config=config.profiler.sampling,
    )

    target_args = (
        config.profiler.filepath,
        config.profiler.args,
        config.profiler.kwargs,
    )
    target_kwargs = {"function_name": config.profiler.entrypoint, **executor_hooks}

    logger.debug(f"Using config: {config}")
    logger.debug(f"Enabled trace hooks: {trace_hooks.keys()}")
    logger.debug(f"Enabled metrics: {config.profiler.enabled_metrics}")
    logger.debug(f"Using args: {config.profiler.args}")
    logger.debug(f"Using kwargs: {config.profiler.kwargs}")
    logger.debug(f"Using entrypoint: {config.profiler.entrypoint}")
    logger.debug(f"Storing buffer files in: {buffer.temp_dir.name}")

    logger.info(f'Starting profiler execution for "{config.profiler.filepath}"')

    run_subprocess(execute_file, sync=True, *target_args, **target_kwargs)

    logger.info("Profiler execution finished")
    logger.debug(f"Amount of buffered file traces: {buffer.buffered_files}")
    logger.info("Saving profile data")

    metadata = build_metadata(
        signature=config.profiler.signature,
        args=config.profiler.args,
        kwargs=config.profiler.kwargs,
    )
    profile_filepath = f"{config.output_dir}/{config.profiler.session_id}.prof"
    build_profile(metadata, buffer.temp_dir.name, profile_filepath)

    logger.debug(f"Using metadata: {metadata}")
    logger.info(f"Profiler output saved to: {config.output_dir}")
