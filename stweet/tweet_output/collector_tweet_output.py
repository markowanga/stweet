"""TweetOutput which saves tweet data in memory, after request can return all saved tweets."""
from typing import List

from .tweet_output import TweetOutput
from ..model import Tweet


class CollectorTweetOutput(TweetOutput):
    """TweetOutput which print first tweet from request batch."""

    _tweets: List[Tweet]

    def __init__(self):
        """Constructor of class, initialize tweets as empty list."""
        self._tweets = []

    def export_tweets(self, tweets: List[Tweet]):
        """Method print first tweet in console, when tweets list is empty there message will be printed."""
        self._tweets.extend(tweets)
        return

    def get_scrapped_tweets(self) -> List[Tweet]:
        """Method returns all collected tweets."""
        return self._tweets
