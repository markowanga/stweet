from typing import List

from model.tweet import Tweet
from tweet_output.tweet_output import TweetOutput


class JsonLineFileTweetOutput(TweetOutput):
    file_name: str

    def export_tweets(self, tweets: List[Tweet]):
        with open(self.file_name, 'w+') as file:
            for tweet in tweets:
                file.write(tweet.to_json_string() + '\n')
        return
