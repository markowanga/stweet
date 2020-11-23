import re
import string
import sys
import unicodedata
from datetime import datetime
from io import StringIO
from typing import List

import pytest

import stweet as st
import stweet.auth
import stweet.exceptions
import stweet.file_reader.read_from_file
from stweet import TweetOutput
from tests.mock_web_client import MockWebClient
from tests.test_util import get_temp_test_file_name, remove_all_temp_files
from tests.tweet_output_counter import TweetOutputCounter


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    remove_all_temp_files()


def get_tweets_to_serialization_test(tweet_output: List[TweetOutput]):
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        all_words=phrase,
        since=datetime(2020, 11, 21),
        until=datetime(2020, 11, 22),
        language=st.Language.POLISH
    )
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=tweet_output
    ).run()


def test_return_tweets_objects():
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        all_words=phrase,
        since=datetime(2020, 11, 18),
        until=datetime(2020, 11, 19),
        language=st.Language.POLISH
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
        from_username=username,
        since=datetime(2020, 10, 1),
        until=datetime(2020, 11, 1)
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
    for index in range(len(tweets_from_csv)):
        if tweets_from_csv[index] != tweets_collector.get_scrapped_tweets()[index]:
            print(tweets_from_csv[index])
            print(tweets_collector.get_scrapped_tweets()[index])
            print('-------')
    assert tweets_from_csv == tweets_collector.get_scrapped_tweets()


def scrap_tweets_with_count(count: int) -> List[st.Tweet]:
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        all_words=phrase,
        since=datetime(2020, 11, 18),
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


def test_get_auth_token_with_incorrect_response_1():
    with pytest.raises(stweet.exceptions.RefreshTokenException):
        stweet.auth.twitter_auth_token_provider.TwitterAuthTokenProvider(MockWebClient(None, None)).refresh()


def test_get_auth_token_with_incorrect_response_2():
    with pytest.raises(stweet.exceptions.RefreshTokenException):
        stweet.auth.twitter_auth_token_provider.TwitterAuthTokenProvider(MockWebClient(400, 'None')).refresh()


def test_get_auth_token_with_incorrect_response_3():
    with pytest.raises(stweet.exceptions.RefreshTokenException):
        stweet.auth.twitter_auth_token_provider.TwitterAuthTokenProvider(MockWebClient(200, 'None')).refresh()


def test_runner_exceptions():
    class TokenExpiryExceptionWebClient(st.WebClient):
        count_dict = dict({
            'https://twitter.com': 0,
            'https://api.twitter.com/2/search/adaptive.json': 0
        })

        def run_request(self, params: st.http_request.RequestDetails) -> st.http_request.RequestResponse:
            self.count_dict[params.url] = self.count_dict[params.url] + 1
            if params.url == 'https://api.twitter.com/2/search/adaptive.json':
                if self.count_dict[params.url] == 1:
                    return st.http_request.RequestResponse(429, None)
                else:
                    return st.http_request.RequestResponse(400, '')
            else:
                return st.http_request.RequestResponse(200, 'decodeURIComponent("gt=1330640566170869763; Max=10800;')

    with pytest.raises(stweet.exceptions.ScrapBatchBadResponse):
        search_tweets_task = st.SearchTweetsTask(
            all_words='#koronawirus'
        )
        st.TweetSearchRunner(
            search_tweets_task=search_tweets_task,
            tweet_outputs=[],
            web_client=TokenExpiryExceptionWebClient()
        ).run()


def remove_accented_chars(text) -> str:
    new_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return new_text


def to_base_text(value: str) -> str:
    table = str.maketrans(dict.fromkeys(string.punctuation))
    to_return = remove_accented_chars(value.translate(table).lower())
    return to_return


def test_exact_words():
    exact_phrase = 'duda kaczyński kempa'
    search_tweets_task = st.SearchTweetsTask(
        exact_words=exact_phrase
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector, st.PrintTweetOutput()]
    ).run()
    assert len(tweets_collector.get_scrapped_tweets()) > 0
    assert all([
        to_base_text(exact_phrase) in to_base_text(tweet.full_text)
        for tweet in tweets_collector.get_scrapped_tweets()
    ]) is True


def contains_any_word(words: str, value: str) -> bool:
    return any([to_base_text(word) in to_base_text(value) for word in words.split()]) is True


def test_any_word():
    any_phrase = 'kaczynski tusk'
    search_tweets_task = st.SearchTweetsTask(
        any_word=any_phrase,
        tweets_count=100
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector, st.PrintTweetOutput()]
    ).run()

    assert len(tweets_collector.get_scrapped_tweets()) > 0
    assert all([
        contains_any_word(any_phrase, tweet.full_text) or contains_any_word(any_phrase, tweet.user_full_name) or
        contains_any_word(any_phrase, tweet.user_name)
        for tweet in tweets_collector.get_scrapped_tweets()
    ]) is True


def test_search_to_username():
    username = 'realDonaldTrump'
    search_tweets_task = st.SearchTweetsTask(
        to_username=username,
        tweets_count=100
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    assert len(tweets_collector.get_scrapped_tweets()) > 0
    assert all([
        to_base_text(username) in to_base_text(tweet.full_text)
        for tweet in tweets_collector.get_scrapped_tweets()
    ]) is True


def run_scrap_test_covid_tweets_in_language(language: st.Language):
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_count=100,
        language=language
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector, st.PrintTweetOutput()]
    ).run()
    assert all([it.lang == language.short_value for it in tweets_collector.get_scrapped_tweets()]) is True


def test_scrap_tweets_in_english():
    run_scrap_test_covid_tweets_in_language(st.Language.ENGLISH)


def test_scrap_tweets_in_polish():
    run_scrap_test_covid_tweets_in_language(st.Language.ENGLISH)


def test_scrap_tweets_in_german():
    run_scrap_test_covid_tweets_in_language(st.Language.GERMAN)


def extract_links(value: str) -> List[str]:
    return re.findall(r'(https?://\S+)', value)


def test_search_with_links():
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_count=500,
        link_filter=st.LinkFilter.ONLY_WITH_LINKS
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector, st.PrintTweetOutput()]
    ).run()
    assert all([
        len(extract_links(it.full_text)) > 0 or it.quoted_status_expand_url is not ''
        for it in tweets_collector.get_scrapped_tweets()
    ]) is True


def test_search_without_links():
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_count=1000,
        link_filter=st.LinkFilter.ONLY_WITHOUT_LINKS
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector, st.PrintTweetOutput()]
    ).run()
    assert all([
        len(extract_links(it.full_text)) == 0 or it.quoted_status_expand_url is ''
        for it in tweets_collector.get_scrapped_tweets()
    ]) is True
