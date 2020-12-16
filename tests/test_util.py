import glob
import os
import string
import unicodedata
import uuid
from typing import List, Callable

import stweet as st

_temp_file_prefix = 'test_temp_file_'


def get_temp_test_file_name(file_extension_without_dot: str) -> str:
    return '{}{}.{}'.format(_temp_file_prefix, _get_uuid_str(), file_extension_without_dot)


def _get_uuid_str() -> str:
    return str(uuid.uuid4()).replace('-', '')


def remove_all_temp_files():
    files_to_remove = glob.glob("{}*".format(_temp_file_prefix))
    for filePath in files_to_remove:
        os.remove(filePath)
    return


def _remove_accented_chars(text) -> str:
    new_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return new_text


def to_base_text(value: str) -> str:
    table = str.maketrans(dict.fromkeys(string.punctuation))
    to_return = _remove_accented_chars(value.translate(table).lower())
    return to_return


def get_tweets_to_tweet_output_test(tweet_output: List[st.TweetOutput]):
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        all_words=phrase,
        tweets_limit=200
    )
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=tweet_output
    ).run()


def get_users_to_tweet_output_test(user_outputs: List[st.UserOutput]) -> st.GetUsersResult:
    users = ['RealDonaldTrump', 'ProtasiewiczJ', 'donaldtuskEPP', 'RealDonaldTrump', 'ProtasiewiczJ', 'donaldtuskEPP']
    get_users_task = st.GetUsersTask(users)
    return st.GetUsersRunner(
        get_user_task=get_users_task,
        user_outputs=user_outputs
    ).run()


def tweet_list_assert_condition(tweets: List[st.Tweet], condition: Callable[[st.Tweet], bool]):
    for tweet in tweets:
        if not condition(tweet):
            print(f'--- {tweet}')
    assert all([
        condition(tweet)
        for tweet in tweets
    ]) is True


def two_lists_assert_equal(tweets_1: List[any], tweets_2: List[any]):
    assert len(tweets_1) == len(tweets_2)
    for tweet_id in range(len(tweets_1)):
        if tweets_1[tweet_id] != tweets_2[tweet_id]:
            print('-----')
            print(tweets_1[tweet_id])
            print(tweets_2[tweet_id])
            print('--')
    assert tweets_1 == tweets_2
