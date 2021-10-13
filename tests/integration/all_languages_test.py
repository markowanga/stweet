import stweet as st
from tests.test_util import tweet_list_assert_condition


def run_test_for_single_language(language: st.Language):
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_limit=10,
        language=language
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    tweet_list_assert_condition(
        tweets_collector.get_raw_list(),
        lambda tweet: tweet.lang in language.short_value
    )


def test_search_in_all_languages():
    for language in st.Language:
        run_test_for_single_language(language)
