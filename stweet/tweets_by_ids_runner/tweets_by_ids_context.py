"""Domain TweetsByIdsContext class."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TweetsByIdsContext:
    """Domain TweetsByIdsContext class."""

    guest_auth_token: Optional[str]
    all_download_tweets_count: int

    def __init__(
            self,
            guest_auth_token: Optional[str] = None,
            all_download_tweets: int = 0
    ):
        """Class constructor."""
        self.guest_auth_token = guest_auth_token
        self.all_download_tweets_count = all_download_tweets
        return

    def add_downloaded_tweets_count(self, new_tweets_count: int):
        """Add download tweet to context counter."""
        self.all_download_tweets_count += new_tweets_count
