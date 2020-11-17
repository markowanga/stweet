from abc import ABC, abstractmethod
from typing import List

from model.tweet import Tweet


class TweetOutput(ABC):

    @abstractmethod
    def export_tweets(self, tweets: List[Tweet]):
        pass
