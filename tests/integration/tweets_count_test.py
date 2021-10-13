from typing import List

import stweet as st


def _scrap_tweets_with_count_assert(count: int):
    phrase = '#covid19'
    search_tweets_task = st.SearchTweetsTask(
        all_words=phrase,
        tweets_limit=count
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    assert len(tweets_collector.get_raw_list()) == count


def test_scrap_small_count_of_tweets():
    _scrap_tweets_with_count_assert(10)


def test_scrap_medium_count_of_tweets():
    _scrap_tweets_with_count_assert(100)


def test_scrap_big_count_of_tweets():
    _scrap_tweets_with_count_assert(299)
