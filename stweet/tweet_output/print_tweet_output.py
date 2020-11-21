"""TweetOutput which print all tweets from request batch."""

from typing import List

from .tweet_output import TweetOutput
from ..model.tweet import Tweet


class PrintTweetOutput(TweetOutput):
    """TweetOutput which print all tweets from request batch."""

    def export_tweets(self, tweets: List[Tweet]):
        """Print all tweets from list."""
        for it in tweets:
            print(it)
        return
