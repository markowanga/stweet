"""Methods to read tweets from files."""

import json
from typing import List

import pandas as pd

from ..model.tweet import Tweet


def read_from_csv(file_path: str) -> List[Tweet]:
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
    return [Tweet.create_tweet_from_flat_dict(row) for _, row in df.iterrows()]


def read_from_json_lines(file_path: str) -> List[Tweet]:
    """Method to read tweets from csv file."""
    file = open(file_path, 'r')
    return [Tweet.create_tweet_from_dict(json.loads(line)) for line in file.readlines()]
