"""Domain TweetsByIdsContext class."""

from dataclasses import dataclass
from typing import Optional

from ..model.cursor import Cursor


@dataclass
class TweetsByIdContext:
    """Domain TweetsByIdsContext class."""

    all_download_tweets_count: int
    requests_count: int
    cursor: Optional[Cursor]

    def __init__(
            self,
            all_download_tweets: int = 0,
            cursor: Optional[Cursor] = None,
            requests_count: int = 0
    ):
        """Class constructor."""
        self.all_download_tweets_count = all_download_tweets
        self.cursor = cursor
        self.requests_count = requests_count
        return

    def add_downloaded_tweets_count_in_request(self, new_tweets_count: int):
        """Add download tweet to context counter."""
        self.all_download_tweets_count += new_tweets_count
        self.requests_count += 1
