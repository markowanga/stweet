"""Domain SearchRunContext class."""

from dataclasses import dataclass
from typing import Optional

from ..model.cursor import Cursor


@dataclass
class SearchRunContext:
    """Domain SearchRunContext class."""

    cursor: Optional[Cursor]
    last_tweets_download_count: int
    all_download_tweets_count: int

    def __init__(
            self,
            cursor: [Cursor] = None,
            guest_auth_token: Optional[str] = None,
            last_tweets_download_count: int = 0,
            all_download_tweets: int = 0
    ):
        """Class constructor."""
        self.cursor = cursor
        self.guest_auth_token = guest_auth_token
        self.last_tweets_download_count = last_tweets_download_count
        self.all_download_tweets_count = all_download_tweets
        return

    def add_downloaded_tweets_count(self, new_downloaded_tweets_count: int):
        """Method to update downloaded tweets count."""
        self.all_download_tweets_count += new_downloaded_tweets_count
        self.last_tweets_download_count = new_downloaded_tweets_count
