from datetime import datetime

from dateutil import parser

import stweet as st
from tests.test_util import tweet_list_assert_condition


def test_between_dates():
    since = datetime(2020, 6, 11, 7, 0, 0, 0)
    until = datetime(2020, 6, 11, 8, 0, 0, 0)
    search_tweets_task = st.SearchTweetsTask(
        any_word="#koronawirus #covid19",
        since=since,
        until=until
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    tweet_list_assert_condition(
        tweets_collector.get_scrapped_tweets(),
        lambda tweet: since.astimezone() <= parser.parse(tweet.created_at).astimezone() <= until.astimezone()
    )
