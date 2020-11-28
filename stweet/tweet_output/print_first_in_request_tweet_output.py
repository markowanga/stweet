"""TweetOutput which print first tweet from request batch."""

from typing import List

from .tweet_output import TweetOutput
from ..model.tweet import Tweet


class PrintFirstInRequestTweetOutput(TweetOutput):
    """TweetOutput which print first tweet from request batch."""

    def export_tweets(self, tweets: List[Tweet]):
        """Method print first tweet in console, when tweets list is empty there message will be printed."""
        message = str(tweets[0]) if len(tweets) > 0 else 'PrintFirstInRequestTweetOutput -- no tweets to print'
        print(message)
        return
