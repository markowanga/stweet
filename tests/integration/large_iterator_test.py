import pytest

import stweet as st
from tests.test_util import get_temp_test_file_name, two_lists_assert_equal, get_tweets_to_tweet_output_test
from tests.test_util import get_users_to_tweet_output_test


def test_user_json_lines_read_iterator():
    file_name = get_temp_test_file_name('jl')
    collector = st.CollectorUserOutput()
    get_users_to_tweet_output_test([collector, st.JsonLineFileUserOutput(file_name)])
    iterator = st.UserJsonLineFileIterator(file_name, 2)
    list_from_iterator = []
    iterator.open()
    while True:
        try:
            list_from_iterator.extend(next(iterator))
        except StopIteration:
            break
    iterator.close()
    two_lists_assert_equal(list_from_iterator, collector.get_scrapped_users())


def test_user_csv_read_iterator():
    file_name = get_temp_test_file_name('csv')
    collector = st.CollectorUserOutput()
    get_users_to_tweet_output_test([collector, st.CsvUserOutput(file_name)])
    iterator = st.UserCsvFileIterator(file_name, 4)
    list_from_iterator = []
    iterator.open()
    while True:
        try:
            list_from_iterator.extend(next(iterator))
        except StopIteration:
            break
    two_lists_assert_equal(list_from_iterator, collector.get_scrapped_users())


def test_tweet_json_lines_read_iterator():
    file_name = get_temp_test_file_name('jl')
    collector = st.CollectorTweetOutput()
    get_tweets_to_tweet_output_test([collector, st.JsonLineFileTweetOutput(file_name)])
    iterator = st.TweetJsonLineFileIterator(file_name, 4)
    list_from_iterator = []
    iterator.open()
    while True:
        try:
            list_from_iterator.extend(next(iterator))
        except StopIteration:
            break
    iterator.close()
    two_lists_assert_equal(list_from_iterator, collector.get_raw_list())


def test_tweet_csv_read_iterator():
    file_name = get_temp_test_file_name('csv')
    collector = st.CollectorTweetOutput()
    get_tweets_to_tweet_output_test([collector, st.CsvTweetOutput(file_name)])
    iterator = st.TweetCsvFileIterator(file_name, 4)
    list_from_iterator = []
    iterator.open()
    while True:
        try:
            list_from_iterator.extend(next(iterator))
        except StopIteration:
            break
    two_lists_assert_equal(list_from_iterator, collector.get_raw_list())
