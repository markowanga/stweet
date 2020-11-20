from datetime import datetime

import pytest

import stweet as st
import stweet.file_reader.read_from_file
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
        language=st.Language.POLISH
    )
    result = st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[]
    ).run()
    assert isinstance(result, SearchTweetsResult)
    assert result.downloaded_count == len(result.tweets)
    assert result.downloaded_count > 0
    assert all([phrase in it.full_text for it in result.tweets if phrase in it.full_text]) is True


def test_return_tweets_from_user():
    username = 'realDonaldTrump'
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=None,
        from_username=username,
        to_username=None,
        since=datetime(2020, 10, 1),
        until=datetime(2020, 11, 1),
        language=None
    )
    result = st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[]
    ).run()
    print(result.tweets[0].user_name)
    assert all([it.user_name == username for it in result.tweets]) is True


def test_no_return_tweets():
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=phrase,
        from_username=None,
        to_username=None,
        since=datetime(2020, 11, 18),
        until=None,
        language=st.Language.POLISH
    )
    result = st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[],
        return_scrapped_objects=False
    ).run()
    assert isinstance(result, SearchTweetsResult)
    assert result.tweets is None


def test_csv_serialization():
    phrase = '#koronawirus'
    csv_filename = get_temp_test_file_name('csv')
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=phrase,
        from_username=None,
        to_username=None,
        since=datetime(2020, 11, 18),
        until=None,
        language=st.Language.POLISH
    )
    result = st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[
            st.CsvTweetOutput(csv_filename)
        ],
        return_scrapped_objects=True
    ).run()
    tweets_from_csv = st.file_reader.read_from_file.read_from_csv(csv_filename)
    assert tweets_from_csv[0] == result.tweets[0]
