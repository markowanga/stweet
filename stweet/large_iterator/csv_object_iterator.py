"""Iterator of objects in csv file."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Iterator, Optional, List

import pandas as pd

T = TypeVar('T')


class CsvObjectIterator(Generic[T], ABC, Iterator):
    """Iterator of objects in csv file."""

    file_path: str
    df_iterator: Optional[Iterator[pd.DataFrame]]
    chunk_size: int

    def __init__(self, file_path: str, chunk_size: int):
        """Constructor of ObjectFileIterator."""
        self.file_path = file_path
        self.df_iterator = None
        self.chunk_size = chunk_size

    def open(self):
        """Method opens fileIterator."""
        self.df_iterator = self._load_df_iterator(self.file_path, self.chunk_size)

    def close(self):
        """Method closes fileIterator."""
        self.df_iterator = None

    @abstractmethod
    def _load_df_iterator(self, file_path: str, chunk_size: int) -> Iterator[pd.DataFrame]:
        """Method loads chunked df iterator."""

    @abstractmethod
    def _df_to_objects(self, df: pd.DataFrame) -> List[T]:
        """Abstract method to parse line to object."""

    def __next__(self) -> List[T]:
        """Iterator method next."""
        df = next(self.df_iterator)
        return self._df_to_objects(df)
