import logging
import inspect


def setup_logger(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def get_module_logger():
    import_stack = inspect.stack()
    importing_module_path = import_stack[1][1]
    importing_module_application_path = importing_module_path.split("experiments")[-1]
    importing_module_name = importing_module_application_path.split(".")[0].replace(
        "/", "."
    )[1:]

    return logging.getLogger(importing_module_name)
