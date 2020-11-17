from typing import List

from stweet.model.tweet import Tweet
from stweet.tweet_output.tweet_output import TweetOutput


class PrintTweetOutput(TweetOutput):

    def export_tweets(self, tweets: List[Tweet]):
        for it in tweets:
            print(it)
        return
