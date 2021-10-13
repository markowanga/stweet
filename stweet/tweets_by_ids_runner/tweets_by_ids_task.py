"""Domain TweetsByIdsTask class."""
from dataclasses import dataclass


@dataclass(frozen=True)
class TweetsByIdTask:
    """Domain TweetsByIdsTask class."""

    tweet_id: str

    def __init__(
            self,
            tweet_id: str
    ):
        """Class constructor."""
        object.__setattr__(self, 'tweet_id', tweet_id)
        return
