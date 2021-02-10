import stweet as st
from tests.test_util import get_temp_test_file_name, two_lists_assert_equal, get_tweets_to_tweet_output_test
from tests.test_util import get_users_to_tweet_output_test


def test_user_json_lines_read_iterator():
    file_name = get_temp_test_file_name('jl')
    collector = st.CollectorUserOutput()
    get_users_to_tweet_output_test([collector, st.JsonLineFileUserOutput(file_name)])
    iterator = st.UserJsonLineFileIterator(file_name)
    list_from_iterator = []
    iterator.open()
    while True:
        try:
            list_from_iterator.append(next(iterator))
        except StopIteration:
            break
    iterator.close()
    two_lists_assert_equal(list_from_iterator, collector.get_scrapped_users())


def test_tweet_json_lines_read_iterator():
    file_name = get_temp_test_file_name('jl')
    collector = st.CollectorTweetOutput()
    get_tweets_to_tweet_output_test([collector, st.JsonLineFileTweetOutput(file_name)])
    iterator = st.TweetJsonLineFileIterator(file_name)
    list_from_iterator = []
    iterator.open()
    while True:
        try:
            list_from_iterator.append(next(iterator))
        except StopIteration:
            break
    iterator.close()
    two_lists_assert_equal(list_from_iterator, collector.get_scrapped_tweets())
