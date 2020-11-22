import sys
from datetime import datetime
from io import StringIO
from typing import List

import pytest

import stweet as st
import stweet.file_reader.read_from_file
from stweet import TweetOutput
from tests.test_util import get_temp_test_file_name, remove_all_test_temp_files
from tests.tweet_output_counter import TweetOutputCounter


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    remove_all_test_temp_files()


def get_tweets_to_serialization_test(tweet_output: List[TweetOutput]):
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        simple_search_phrase=phrase,
        from_username=None,
        to_username=None,
        since=datetime(2020, 11, 21),
        until=datetime(2020, 11, 22),
        language=st.Language.POLISH,
        tweets_count=None
    )
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=tweet_output
    ).run()


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
    assert isinstance(result, st.SearchTweetsResult)
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
    csv_filename = get_temp_test_file_name('csv')
    tweets_collector = st.CollectorTweetOutput()
    get_tweets_to_serialization_test([
        st.CsvTweetOutput(csv_filename),
        tweets_collector
    ])
    tweets_from_csv = st.file_reader.read_from_file.read_from_csv(csv_filename)
    assert tweets_from_csv == tweets_collector.get_scrapped_tweets()


def scrap_tweets_with_count(count: int) -> List[st.Tweet]:
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
    tweets_count = 299
    assert len(scrap_tweets_with_count(tweets_count)) == tweets_count


def test_unique_language_shortcut():
    assert len(st.Language) == len(set([it.short_value for it in st.Language]))


def test_file_json_lines_serialization():
    jl_filename = get_temp_test_file_name('jl')
    tweets_collector = st.CollectorTweetOutput()
    get_tweets_to_serialization_test([
        st.JsonLineFileTweetOutput(jl_filename),
        tweets_collector
    ])
    tweets_from_jl = st.file_reader.read_from_file.read_from_json_lines(jl_filename)
    assert len(tweets_from_jl) == len(tweets_collector.get_scrapped_tweets())
    assert tweets_from_jl == tweets_collector.get_scrapped_tweets()


def test_print_all_tweet_output():
    captured_output = StringIO()
    sys.stdout = captured_output
    tweets_collector = st.CollectorTweetOutput()
    get_tweets_to_serialization_test([
        st.PrintTweetOutput(),
        tweets_collector
    ])
    sys.stdout = sys.__stdout__
    captured_output.getvalue().count('Tweet(')
    assert captured_output.getvalue().count('Tweet(') == len(tweets_collector.get_scrapped_tweets())


def test_print_batch_single_tweet_tweet_output():
    captured_output = StringIO()
    sys.stdout = captured_output
    tweet_output_counter = TweetOutputCounter()
    get_tweets_to_serialization_test([
        st.PrintFirstInRequestTweetOutput(),
        tweet_output_counter
    ])
    sys.stdout = sys.__stdout__
    captured_output.getvalue().count('Tweet(')
    print_tweet_count = captured_output.getvalue().count('Tweet(')
    print_no_tweets_line = captured_output.getvalue().count('PrintFirstInRequestTweetOutput -- no tweets to print')
    assert (print_tweet_count + print_no_tweets_line) == tweet_output_counter.get_output_call_count()
