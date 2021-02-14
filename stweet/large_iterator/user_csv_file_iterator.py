"""Iterator to parse Tweet from JSON lines."""
from typing import Iterator, List

import pandas as pd

from .csv_object_iterator import CsvObjectIterator
from .. import User
from ..import_data.users_import import df_to_users, get_users_df_chunked


class TweetCsvFileIterator(CsvObjectIterator[User]):
    """Iterator to parse Tweet from JSON lines."""

    def __init__(self, file_path: str, chunk_size: int):
        super().__init__(file_path, chunk_size)

    def _load_df_iterator(self, file_path: str, chunk_size: int) -> Iterator[pd.DataFrame]:
        return get_users_df_chunked(file_path, chunk_size)

    def _df_to_objects(self, df: pd.DataFrame) -> List[User]:
        return df_to_users(df)
