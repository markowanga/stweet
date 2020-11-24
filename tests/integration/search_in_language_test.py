import stweet as st


def _run_search_test_covid_tweets_in_language(language: st.Language):
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
    assert all([
        it.lang == language.short_value
        for it in tweets_collector.get_scrapped_tweets()
    ]) is True


def test_search_tweets_in_english():
    _run_search_test_covid_tweets_in_language(st.Language.ENGLISH)


def test_search_tweets_in_polish():
    _run_search_test_covid_tweets_in_language(st.Language.ENGLISH)


def test_search_tweets_in_german():
    _run_search_test_covid_tweets_in_language(st.Language.GERMAN)
