"""TweetOutput which print all tweets from request batch."""

from typing import List

from stweet.model.tweet import Tweet
from stweet.tweet_output.tweet_output import TweetOutput


class PrintTweetOutput(TweetOutput):
    """TweetOutput which print all tweets from request batch."""

    def export_tweets(self, tweets: List[Tweet]):
        """Print all tweets from list."""
        for it in tweets:
            print(it)
        return
