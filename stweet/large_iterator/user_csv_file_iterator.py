"""Iterator to parse User from CSV."""
from typing import Iterator, List

import pandas as pd

from .csv_object_iterator import CsvObjectIterator
from ..model import User
from ..import_data.users_import import df_to_users, get_users_df_chunked


class UserCsvFileIterator(CsvObjectIterator[User]):
    """Iterator to parse User from CSV."""

    def __init__(self, file_path: str, chunk_size: int):
        """Constructor of UserCsvFileIterator."""
        super().__init__(file_path, chunk_size)

    def _load_df_iterator(self, file_path: str, chunk_size: int) -> Iterator[pd.DataFrame]:
        """Method loads df iterator."""
        return get_users_df_chunked(file_path, chunk_size)

    def _df_to_objects(self, df: pd.DataFrame) -> List[User]:
        """Method converts ."""
        return df_to_users(df)
