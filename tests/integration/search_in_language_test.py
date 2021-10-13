import stweet as st
from tests.test_util import tweet_list_assert_condition


def _run_search_test_covid_tweets_in_language(language: st.Language):
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_limit=100,
        language=language
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    tweet_list_assert_condition(
        tweets_collector.get_raw_list(),
        lambda tweet: tweet.lang == language.short_value
    )


def test_search_tweets_in_english():
    _run_search_test_covid_tweets_in_language(st.Language.ENGLISH)


def test_search_tweets_in_polish():
    _run_search_test_covid_tweets_in_language(st.Language.ENGLISH)


def test_search_tweets_in_german():
    _run_search_test_covid_tweets_in_language(st.Language.GERMAN)
