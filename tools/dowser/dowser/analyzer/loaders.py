import pandas as pd


__all__ = ["load_session"]


def load_session(session_path: str) -> pd.DataFrame:
    return pd.read_parquet(session_path)
