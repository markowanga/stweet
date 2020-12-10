"""Domain TweetsByIdsTask class."""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TweetsByIdsTask:
    """Domain TweetsByIdsTask class."""

    tweet_ids: List[str]

    def __init__(
            self,
            tweet_ids: List[str]
    ):
        """Class constructor."""
        object.__setattr__(self, 'tweet_ids', tweet_ids)
        return
