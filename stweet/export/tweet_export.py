"""Methods to export tweets."""
from typing import List

from .util import clear_file
from .. import JsonLineFileTweetOutput
from ..model import Tweet
from ..tweet_output import CsvTweetOutput


def export_tweets_to_csv(tweets: List[Tweet], filename: str):
    """Method to export tweets to csv."""
    clear_file(filename)
    CsvTweetOutput(filename).export_tweets(tweets)
    return


def export_tweets_to_json_lines(tweets: List[Tweet], filename: str):
    """Method to export tweets to json lines file."""
    clear_file(filename)
    JsonLineFileTweetOutput(filename).export_tweets(tweets)
    return
