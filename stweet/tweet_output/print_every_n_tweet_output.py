"""TweetOutput which print each n-th tweet."""

from typing import List

from .tweet_output import TweetOutput
from ..model.tweet import Tweet


class PrintEveryNTweetOutput(TweetOutput):
    """TweetOutput which print each n-th tweet."""

    each_n: int
    _counter: int = 0

    def __init__(self, each_n: int):
        """Create instance of PrintEveryNTweetOutput."""
        self.each_n = each_n

    def export_tweets(self, tweets: List[Tweet]):
        """Method print first each n tweet in console with all scrapped count."""
        for it in tweets:
            self._counter += 1
            if self._counter % self.each_n == 0:
                print(self._counter, it)
        return
