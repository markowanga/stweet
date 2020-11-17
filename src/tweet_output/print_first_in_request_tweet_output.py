"""TweetOutput which print first tweet from request batch."""

from typing import List

from model.tweet import Tweet
from tweet_output.tweet_output import TweetOutput


class PrintFirstInRequestTweetOutput(TweetOutput):
    """TweetOutput which print first tweet from request batch."""

    def export_tweets(self, tweets: List[Tweet]):
        """Method print first tweet in console, when tweets list is empty there message will be printed."""
        if len(tweets) > 0:
            print(tweets[0])
        else:
            print('PrintFirstInRequestTweetOutput -- no tweets to print')
        return
