"""Methods to read tweets from files."""

from typing import List

import pandas as pd

from ..mapper.tweet_dict_mapper import create_tweet_from_flat_dict
from ..mapper.tweet_json_mapper import create_tweet_from_json
from ..model.tweet import Tweet


def read_tweets_from_csv_file(file_path: str) -> List[Tweet]:
    """Method to read tweets from csv file."""
    df = pd.read_csv(file_path, dtype={
        'quoted_status_id_str': str,
        'in_reply_to_status_id_str': str,
        'in_reply_to_user_id_str': str
    })
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
