"""Methods to read tweets from files."""

from io import StringIO
from typing import List, Union, Iterator

import pandas as pd

from ..mapper.tweet_dict_mapper import create_tweet_from_flat_dict
from ..mapper.tweet_json_mapper import create_tweet_from_json
from ..model.tweet import Tweet

_TWEET_DF_DTYPE = {
    'quoted_status_id_str': str,
    'in_reply_to_status_id_str': str,
    'in_reply_to_user_id_str': str,
    'media_url': str
}


def read_tweets_from_csv_file(file_path: str) -> List[Tweet]:
    """Method to read tweets from csv file."""
    return _read_tweets_from_csv_object(file_path)


def read_tweets_from_csv_buffer(buffer: StringIO) -> List[Tweet]:
    """Method to read tweets from csv string buffer."""
    return _read_tweets_from_csv_object(buffer)


def get_tweets_df_chunked(file_path: str, chunk_size: int) -> Iterator[pd.DataFrame]:
    """Method to read tweets from csv file or buffer."""
    return pd.read_csv(file_path, dtype=_TWEET_DF_DTYPE, chunksize=chunk_size)


def _read_tweets_from_csv_object(filepath_or_buffer_path: Union[str, StringIO]) -> List[Tweet]:
    """Method to read tweets from csv file or buffer."""
    df = pd.read_csv(filepath_or_buffer_path, dtype=_TWEET_DF_DTYPE)
    return df_to_tweets(df)


def df_to_tweets(df: pd.DataFrame) -> List[Tweet]:
    """Parse DataFrame to List[Tweet]."""
    if 'media_url' not in df.columns:
        df['media_url'] = ''
    df.quoted_status_id_str.fillna('', inplace=True)
    df.quoted_status_short_url.fillna('', inplace=True)
    df.quoted_status_expand_url.fillna('', inplace=True)
    df.in_reply_to_status_id_str.fillna('', inplace=True)
    df.in_reply_to_user_id_str.fillna('', inplace=True)
    df.hashtags.fillna('', inplace=True)
    df.urls.fillna('', inplace=True)
    df.mentions.fillna('', inplace=True)
    return [create_tweet_from_flat_dict(row) for _, row in df.iterrows()]


def read_tweets_from_json_lines_file(file_path: str) -> List[Tweet]:
    """Method to read tweets from csv file."""
    file = open(file_path, 'r')
    return [create_tweet_from_json(line) for line in file.readlines()]
