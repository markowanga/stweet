from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchRunContext:
    scroll_token: str
    guest_auth_token: Optional[str]
    was_no_more_data_raised: bool
    last_tweets_download_count: int

    def __init__(self, scroll_token: str = '-1', guest_auth_token: Optional[str] = None,
                 was_no_more_data_raised: bool = False, last_tweets_download_count: int = -1):
        self.scroll_token = scroll_token
        self.guest_auth_token = guest_auth_token
        self.was_no_more_data_raised = was_no_more_data_raised
        self.last_tweets_download_count = last_tweets_download_count
