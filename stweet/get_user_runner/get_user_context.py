"""Domain TweetsByIdsContext class."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GetUserContext:
    """Domain TweetsByIdsContext class."""

    guest_auth_token: Optional[str] = None
