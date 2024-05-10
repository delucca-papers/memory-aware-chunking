import os
import dowser
import pandas as pd

from typing import List


def save_plots(directory_path: str, unit: str) -> None:
    sessions = get_sessions(directory_path)
    session_names = get_session_names(sessions)
    zipped_sessions = zip(session_names, sessions)

    dowser.compare_profiles(
        {session_name: session for session_name, session in zipped_sessions},
        unit,
        output_dir=directory_path,
    )


def get_sessions(directory_path: str) -> List[str]:
    dirs = list_directories(directory_path)
    backends = [backend for backend in dirs if "data" not in backend]
    return [find_parquet_files(backend)[0] for backend in backends]


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


def find_parquet_files(directory: str) -> List[str]:
    parquet_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".parquet"):
                full_path = os.path.join(root, file)
                parquet_files.append(full_path)
    return parquet_files


if __name__ == "__main__":
    directory_path = os.environ.get("EXPERIMENT_OUTPUT_DIR")
    unit = os.environ.get("EXPERIMENT_UNIT")

    save_plots(directory_path, unit)
