from arrow import Arrow

import stweet as st
from tests.test_util import tweet_list_assert_condition


def _run_test_between_dates(since: Arrow, until: Arrow):
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
        tweets_collector.get_raw_list(),
        lambda tweet: since <= tweet.created_at <= until
    )


def test_for_polish_timezone():
    _run_test_between_dates(
        since=Arrow(year=2020, month=6, day=11, hour=7),
        until=Arrow(year=2020, month=6, day=11, hour=8)
    )


def test_for_utc_timezone():
    tz = 'Europe/Warsaw'
    _run_test_between_dates(
        since=Arrow(year=2020, month=6, day=11, hour=7, tzinfo=tz),
        until=Arrow(year=2020, month=6, day=11, hour=8, tzinfo=tz)
    )
