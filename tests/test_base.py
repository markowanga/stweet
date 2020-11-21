from datetime import datetime
from typing import List

import pytest

import stweet as st
import stweet.file_reader.read_from_file
from stweet import Tweet
from stweet.model.search_tweets_result import SearchTweetsResult
from tests.test_util import remove_all_temp_files, get_temp_test_file_name


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    remove_all_temp_files()


def test_return_tweets_objects():
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=phrase,
        from_username=None,
        to_username=None,
        since=datetime(2020, 11, 18),
        until=None,
        language=st.Language.POLISH,
        tweets_count=None
    )
    tweets_collector = st.CollectorTweetOutput()
    result = st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    scrapped_tweets = tweets_collector.get_scrapped_tweets()
    assert isinstance(result, SearchTweetsResult)
    assert result.downloaded_count == len(scrapped_tweets)
    assert result.downloaded_count > 0
    assert all([phrase in it.full_text for it in scrapped_tweets if phrase in it.full_text]) is True


def test_return_tweets_from_user():
    username = 'realDonaldTrump'
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=None,
        from_username=username,
        to_username=None,
        since=datetime(2020, 10, 1),
        until=datetime(2020, 11, 1),
        language=None,
        tweets_count=None
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    assert all([it.user_name == username for it in tweets_collector.get_scrapped_tweets()]) is True


def test_csv_serialization():
    phrase = '#koronawirus'
    csv_filename = get_temp_test_file_name('csv')
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=phrase,
        from_username=None,
        to_username=None,
        since=datetime(2020, 11, 18),
        until=None,
        language=st.Language.POLISH,
        tweets_count=None
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[
            st.CsvTweetOutput(csv_filename),
            tweets_collector
        ]
    ).run()
    tweets_from_csv = st.file_reader.read_from_file.read_from_csv(csv_filename)
    assert tweets_from_csv[0] == tweets_collector.get_scrapped_tweets()[0]


def scrap_tweets_with_count(count: int) -> List[Tweet]:
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=phrase,
        from_username=None,
        to_username=None,
        since=datetime(2020, 11, 18),
        until=None,
        language=st.Language.POLISH,
        tweets_count=count
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    return tweets_collector.get_scrapped_tweets()


def test_scrap_small_count_of_tweets():
    tweets_count = 10
    assert len(scrap_tweets_with_count(tweets_count)) == tweets_count


def test_scrap_medium_count_of_tweets():
    tweets_count = 100
    assert len(scrap_tweets_with_count(tweets_count)) == tweets_count


def test_scrap_big_count_of_tweets():
    tweets_count = 999
    assert len(scrap_tweets_with_count(tweets_count)) == tweets_count
