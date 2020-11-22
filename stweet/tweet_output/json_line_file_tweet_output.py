"""TweetOutput which saves tweets as JSON objects."""

from typing import List

from .tweet_output import TweetOutput
from ..model.tweet import Tweet


class JsonLineFileTweetOutput(TweetOutput):
    """TweetOutput which saves tweets as JSON objects.

    TweetOutput which saves tweet data by request received tweets batch to text file.
    Every tweet is saved in one line, this is JSON object.
    """

    file_name: str

    def __init__(self, file_name: str):
        """Creates instance of JsonLineFileTweetOutput."""
        self.file_name = file_name

    def export_tweets(self, tweets: List[Tweet]):
        """Append new tweet JSON strings to file."""
        with open(self.file_name, 'a') as file:
            for tweet in tweets:
                file.write(tweet.to_json_string() + '\n')
        return
