import os
from typing import List

import pandas as pd

from model.tweet import Tweet
from tweet_output.tweet_output import TweetOutput

_fields_list = ['created_at', 'id_str', 'conversation_id_str', 'full_text', 'lang', 'favorited', 'retweeted',
                'retweet_count', 'favorite_count', 'reply_count', 'quote_count', 'user_id_str', 'user_name',
                'user_full_name']


class CsvTweetOutput(TweetOutput):
    file_location: str
    add_header_on_start: bool

    def __init__(self, file_location: str, add_header_on_start: bool = True):
        self.file_location = file_location
        self.add_header_on_start = add_header_on_start

    def export_tweets(self, tweets: List[Tweet]):
        dict_list = [it.__dict__ for it in tweets]
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
