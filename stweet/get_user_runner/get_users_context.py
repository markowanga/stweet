"""Domain TweetsByIdsContext class."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GetUsersContext:
    """Domain TweetsByIdsContext class."""

    guest_auth_token: Optional[str] = None
    scrapped_count: int = 0

    def add_one_scrapped_user(self):
        """Method raise counter of all scrapped tweets."""
        self.scrapped_count += 1
