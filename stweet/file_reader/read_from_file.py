"""Methods to read tweets from files."""

import json
from typing import List

import pandas as pd

from ..model.tweet import Tweet


def read_from_csv(file_path: str) -> List[Tweet]:
    """Method to read tweets from csv file."""
    df = pd.read_csv(file_path)
    return [Tweet.create_tweet_from_dict(row) for _, row in df.iterrows()]


def read_from_json_lines(file_path: str) -> List[Tweet]:
    """Method to read tweets from csv file."""
    file = open(file_path, 'r')
    return [Tweet.create_tweet_from_dict(json.loads(line)) for line in file.readlines()]
