from typing import List

import pytest

import stweet as st
from tests.test_util import get_temp_test_file_name, two_lists_assert_equal

# pytest.fixture(autouse=True)(run_around_tests)


def get_tweets() -> List[st.UserTweetRaw]:
    collect_tweet_output = st.CollectorTweetOutput()
    task = st.SearchTweetsTask(all_words="#covid19", tweets_limit=100)
    st.TweetSearchRunner(task, [collect_tweet_output]).run()
    return collect_tweet_output.get_raw_list()


def get_users() -> List[st.User]:
    collect_user_output = st.CollectorUserOutput()
    task = st.GetUsersTask(list(set([tweet.user_name for tweet in get_tweets()]))[:10])
    st.GetUsersRunner(task, [collect_user_output]).run()
    return collect_user_output.get_scrapped_users()


def test_tweet_json_lines_serialization():
    jl_filename = get_temp_test_file_name('jl')
    tweets = get_tweets()
    st.export_tweets_to_json_lines(tweets, jl_filename)
    imported_tweets = st.read_tweets_from_json_lines_file(jl_filename)
    two_lists_assert_equal(imported_tweets, tweets)


def test_tweet_csv_serialization():
    csv_filename = get_temp_test_file_name('csv')
    tweets = get_tweets()
    st.export_tweets_to_csv(tweets, csv_filename)
    imported_tweets = st.read_tweets_from_csv_file(csv_filename)
    two_lists_assert_equal(imported_tweets, tweets)


def test_user_json_lines_serialization():
    jl_filename = get_temp_test_file_name('jl')
    users = get_users()
    st.export_users_to_json_lines(users, jl_filename)
    imported_tweets = st.read_users_from_json_lines_file(jl_filename)
    two_lists_assert_equal(imported_tweets, users)


def test_user_csv_serialization():
    csv_filename = get_temp_test_file_name('csv')
    users = get_users()
    st.export_users_to_csv(users, csv_filename)
    imported_tweets = st.read_users_from_csv_file(csv_filename)
    two_lists_assert_equal(users, imported_tweets)
