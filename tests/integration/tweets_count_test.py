from typing import List

import stweet as st


def scrap_tweets_with_count(count: int) -> List[st.Tweet]:
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        all_words=phrase,
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
