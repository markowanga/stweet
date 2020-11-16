from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchRunContext:
    scroll_token: str
    guest_auth_token: Optional[str]
    was_no_more_data_raised: bool
    last_tweets_download_count: int
    all_download_tweets: int
    all_filtered_tweets: int

    def __init__(self, scroll_token: str = '-1', guest_auth_token: Optional[str] = None,
                 was_no_more_data_raised: bool = False, last_tweets_download_count: int = -1,
                 all_download_tweets: int = 0, all_filtered_tweets: int = 0):
        self.scroll_token = scroll_token
        self.guest_auth_token = guest_auth_token
        self.was_no_more_data_raised = was_no_more_data_raised
        self.last_tweets_download_count = last_tweets_download_count
        self.all_download_tweets = all_download_tweets
        self.all_filtered_tweets = all_filtered_tweets
        return

    def add_downloaded_tweets_count(self, downloaded_tweets: int, filtered_tweets: int):
        self.all_download_tweets += downloaded_tweets
        self.all_filtered_tweets += filtered_tweets
