"""Domain TweetsByIdsContext class."""

from dataclasses import dataclass
from typing import Optional

from ..model.cursor import Cursor


@dataclass
class TweetsByIdContext:
    """Domain TweetsByIdsContext class."""

    all_download_tweets_count: int
    last_scrapped_tweets_count: int
    cursor: Optional[Cursor]

    def __init__(
            self,
            all_download_tweets: int = 0,
            cursor: Optional[Cursor] = None,
            last_scrapped_tweets_count: int = 0
    ):
        """Class constructor."""
        self.all_download_tweets_count = all_download_tweets
        self.cursor = cursor
        self.last_scrapped_tweets_count = last_scrapped_tweets_count
        return

    def add_downloaded_tweets_count(self, new_tweets_count: int):
        """Add download tweet to context counter."""
        self.all_download_tweets_count += new_tweets_count
        self.last_scrapped_tweets_count = new_tweets_count
