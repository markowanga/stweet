import pytest

import stweet as st
from tests.test_util import get_temp_test_file_name, remove_all_temp_files, get_tweets_to_tweet_output_test, \
    two_lists_assert_equal


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    remove_all_temp_files()


def test_csv_serialization():
    csv_filename = get_temp_test_file_name('csv')
    tweets_collector = st.CollectorTweetOutput()
    get_tweets_to_tweet_output_test([
        st.CsvTweetOutput(csv_filename),
        tweets_collector
    ])
    tweets_from_csv = st.read_tweets_from_csv_file(csv_filename)
    two_lists_assert_equal(tweets_from_csv, tweets_collector.get_scrapped_tweets())


def test_file_json_lines_serialization():
    jl_filename = get_temp_test_file_name('jl')
    tweets_collector = st.CollectorTweetOutput()
    get_tweets_to_tweet_output_test([
        st.JsonLineFileTweetOutput(jl_filename),
        tweets_collector
    ])
    tweets_from_jl = st.read_tweets_from_json_lines_file(jl_filename)
    two_lists_assert_equal(tweets_from_jl, tweets_collector.get_scrapped_tweets())
