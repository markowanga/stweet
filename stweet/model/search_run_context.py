"""Domain SearchRunContext class."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchRunContext:
    """Domain SearchRunContext class."""

    scroll_token: Optional[str]
    guest_auth_token: Optional[str]
    was_no_more_data_raised: bool
    last_tweets_download_count: int
    all_download_tweets_count: int

    def __init__(self, scroll_token: str = '-1', guest_auth_token: Optional[str] = None,
                 was_no_more_data_raised: bool = False, last_tweets_download_count: int = -1,
                 all_download_tweets: int = 0):
        """Class constructor."""
        self.scroll_token = scroll_token
        self.guest_auth_token = guest_auth_token
        self.was_no_more_data_raised = was_no_more_data_raised
        self.last_tweets_download_count = last_tweets_download_count
        self.all_download_tweets_count = all_download_tweets
        return

    def add_downloaded_tweets_count(self, downloaded_tweets_count: int):
        """Method to update downloaded tweets count."""
        self.all_download_tweets_count += downloaded_tweets_count
