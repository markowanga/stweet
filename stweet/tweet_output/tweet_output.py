"""Generic class to process tweet output."""

from abc import ABC, abstractmethod
from typing import List

from ..model.tweet import Tweet


class TweetOutput(ABC):
    """Generic class to process tweet output."""

    @abstractmethod
    def export_tweets(self, tweets: List[Tweet]):
        """Method to process all tweets from request batch."""
