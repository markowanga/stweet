"""Methods to read users from files."""

from io import StringIO
from typing import List, Union, Iterator

import pandas as pd

from ..mapper.user_dict_mapper import create_user_from_flat_dict
from ..mapper.user_json_mapper import create_user_from_json
from ..model import User

_USER_DF_DTYPE = {
    'pinned_tweet_ids_str': str,
    'profile_banner_url': str,
    'location': str,
    'description': str
}


def read_users_from_csv_file(file_path: str) -> List[User]:
    """Method to read tweets from csv file."""
    return _read_users_from_csv(file_path)


def read_users_from_json_lines_file(file_path: str) -> List[User]:
    """Method to read tweets from csv file."""
    file = open(file_path, 'r')
    return [create_user_from_json(line) for line in file.readlines()]


def _read_users_from_csv(csv_input: Union[str, StringIO]) -> List[User]:
    """Method to read tweets from csv buffer or file."""
    df = pd.read_csv(csv_input, dtype=_USER_DF_DTYPE)
    return df_to_users(df)


def get_users_df_chunked(file_path: str, chunk_size: int) -> Iterator[pd.DataFrame]:
    """Method to read tweets from csv file or buffer."""
    return pd.read_csv(file_path, dtype=_USER_DF_DTYPE, chunksize=chunk_size)


def df_to_users(df: pd.DataFrame) -> List[User]:
    """Converts DataFrame to List[User]."""
    df.pinned_tweet_ids_str.fillna('', inplace=True)
    df.profile_banner_url.fillna('', inplace=True)
    df.location.fillna('', inplace=True)
    df.description.fillna('', inplace=True)
    return [create_user_from_flat_dict(row) for _, row in df.iterrows()]
