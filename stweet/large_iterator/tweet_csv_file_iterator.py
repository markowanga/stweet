"""Iterator to parse Tweet from JSON lines."""
from typing import Iterator, List

import pandas as pd

from .csv_object_iterator import CsvObjectIterator
from ..import_data.tweets_import import get_tweets_df_chunked, df_to_tweets
from ..model import Tweet


class TweetCsvFileIterator(CsvObjectIterator[Tweet]):
    """Iterator to parse Tweet from JSON lines."""

    def __init__(self, file_path: str, chunk_size: int):
        """Constructor of TweetCsvFileIterator."""
        super().__init__(file_path, chunk_size)

    def _load_df_iterator(self, file_path: str, chunk_size: int) -> Iterator[pd.DataFrame]:
        return get_tweets_df_chunked(file_path, chunk_size)

    def _df_to_objects(self, df: pd.DataFrame) -> List[Tweet]:
        return df_to_tweets(df)
