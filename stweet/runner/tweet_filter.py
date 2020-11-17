from typing import List

from stweet.model.search_tweets_task import SearchTweetsTask
from stweet.model.tweet import Tweet


class TweetFilter:
    search_tweet_task: SearchTweetsTask

    def __init__(self, search_tweet_task: SearchTweetsTask):
        self.search_tweet_task = search_tweet_task
        return

    def filter_tweets(self, tweets: List[Tweet]) -> List[Tweet]:
        return [it for it in tweets if self.predicate(it)]

    def predicate(self, tweet: Tweet) -> bool:
        return self._predicate_language(tweet)

    def _predicate_language(self, tweet: Tweet) -> bool:
        # print(tweet.lang, self.search_tweet_task.language)
        return tweet.lang is None or tweet.lang == self.search_tweet_task.language.short_value
