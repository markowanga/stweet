import stweet as st
from tests.test_util import to_base_text, tweet_list_assert_condition


def search_by_hashtag():
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        all_words=phrase,
        tweets_limit=200
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    scrapped_tweets = tweets_collector.get_raw_list()
    assert all([phrase in it.full_text for it in scrapped_tweets if phrase in it.full_text]) is True


def test_exact_words():
    exact_phrase = 'duda kaczyński kempa'
    search_tweets_task = st.SearchTweetsTask(
        exact_words=exact_phrase
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    tweet_list_assert_condition(
        tweets_collector.get_raw_list(),
        lambda tweet: to_base_text(exact_phrase) in to_base_text(tweet.full_text)
    )


def contains_any_word(words: str, value: str) -> bool:
    return any([to_base_text(word) in to_base_text(value) for word in words.split()]) is True


def test_any_word():
    any_phrase = 'kaczynski tusk'
    search_tweets_task = st.SearchTweetsTask(
        any_word=any_phrase,
        tweets_limit=100
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()

    tweet_list_assert_condition(
        tweets_collector.get_raw_list(),
        lambda tweet: contains_any_word(any_phrase, tweet.full_text) or contains_any_word(
            any_phrase, tweet.user_full_name) or contains_any_word(any_phrase, tweet.user_name)
    )
