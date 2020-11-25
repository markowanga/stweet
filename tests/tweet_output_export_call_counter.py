from typing import List

import stweet as st


class TweetOutputExportCallCounter(st.TweetOutput):
    counter: int

    def __init__(self):
        self.counter = 0

    def export_tweets(self, tweets: List[st.Tweet]):
        self.counter += 1
        return

    def get_output_call_count(self) -> int:
        return self.counter
