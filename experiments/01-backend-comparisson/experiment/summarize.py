import os
import dowser

from typing import List
from dowser.profiler.loaders import load_profile
from dowser.common.logger import logger


def save_plots(directory_path: str, unit: str) -> None:
    logger.info("Starting to create experiment summary")

    sessions = get_sessions(directory_path)

    logger.debug("Getting session names and building zipped sessions")
    session_names = get_session_names(sessions)
    zipped_sessions = zip(session_names, sessions)

    logger.info("Comparing profiles")
    dowser.compare_profiles(
        {session_name: session for session_name, session in zipped_sessions},
        unit,
        output_dir=directory_path,
    )

def get_sessions(directory_path: str) -> List[str]:
    dirs = list_directories(directory_path)
    backends = [backend for backend in dirs if "data" not in backend]
    return [find_profiles(backend)[0] for backend in backends]


def get_session_names(sessions: List[str]) -> List[str]:
    return [
        os.path.basename(session).split("-")[-1].split(".")[0] for session in sessions
    ]


def list_directories(path: str) -> List[str]:
    entries = os.listdir(path)

    directories = [
        os.path.join(path, entry)
        for entry in entries
        if os.path.isdir(os.path.join(path, entry))
    ]
    return directories


def find_profiles(directory: str) -> List[str]:
    parquet_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".prof"):
                full_path = os.path.join(root, file)
                parquet_files.append(full_path)
    return parquet_files


if __name__ == "__main__":
    directory_path = os.environ.get("EXPERIMENT_OUTPUT_DIR")
    unit = os.environ.get("EXPERIMENT_UNIT")

    save_plots(directory_path, unit)
