"""TweetOutput which saves tweet data by request received tweets batch to CSV file."""

import os
from typing import List

import pandas as pd

from .tweet_output import TweetOutput
from ..model.tweet import Tweet

_fields_list = ['created_at', 'id_str', 'conversation_id_str', 'full_text', 'lang', 'favorited', 'retweeted',
                'retweet_count', 'favorite_count', 'reply_count', 'quote_count', 'quoted_status_id_str',
                'quoted_status_short_url', 'quoted_status_expand_url', 'user_id_str', 'user_name', 'user_full_name',
                'user_verified', 'in_reply_to_status_id_str', 'in_reply_to_user_id_str', 'hashtags', 'mentions',
                'urls']


class CsvTweetOutput(TweetOutput):
    """CsvTweetOutput saves tweet data by request received tweets batch to CSV file."""

    file_location: str
    add_header_on_start: bool

    def __init__(self, file_location: str, add_header_on_start: bool = True):
        """Create instance of CsvTweetOutput."""
        self.file_location = file_location
        self.add_header_on_start = add_header_on_start

    def export_tweets(self, tweets: List[Tweet]):
        """Export tweets to CSV."""
        dict_list = [it.to_flat_dict() for it in tweets]
        df = pd.DataFrame(dict_list, columns=_fields_list)
        df.to_csv(
            path_or_buf=self.file_location,
            mode='a',
            header=self._header_to_add(),
            index=False
        )
        return

    def _header_to_add(self):
        return (not self._file_exists()) or self._file_is_empty()

    def _file_exists(self) -> bool:
        return os.path.isfile(self.file_location)

    def _file_is_empty(self) -> bool:
        return os.stat(self.file_location).st_size == 0
