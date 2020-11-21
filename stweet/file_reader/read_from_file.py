"""Methods to read tweets from files."""

from typing import List

import pandas as pd

from ..model.tweet import Tweet


def read_from_csv(file_path: str) -> List[Tweet]:
    """Method to read tweets from csv file."""
    df = pd.read_csv(file_path)
    return [Tweet.create_tweet_from_dict(row) for _, row in df.iterrows()]
