import pandas as pd
import pyarrow.parquet as pq


__all__ = ["load_session"]


def load_session(session_path: str, include_metadata: bool = True) -> pd.DataFrame:
    table = pq.read_table(session_path)

    df = table.to_pandas()

    if include_metadata:
        metadata = table.schema.metadata
        decoded_metadata = {
            k.decode("utf-8"): v.decode("utf-8") for k, v in metadata.items()
        }
        df.attrs["metadata"] = decoded_metadata

    return df
