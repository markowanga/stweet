import stweet as st
from tests.test_util import to_base_text, tweet_list_assert_condition


def test_search_to_username():
    username = 'realDonaldTrump'
    search_tweets_task = st.SearchTweetsTask(
        to_username=username,
        tweets_limit=100
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    tweet_list_assert_condition(
        tweets_collector.get_raw_list(),
        lambda tweet: to_base_text(username) in to_base_text(tweet.full_text)
    )


def test_return_tweets_from_user():
    username = 'realDonaldTrump'
    search_tweets_task = st.SearchTweetsTask(
        from_username=username,
        tweets_limit=100
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    tweet_list_assert_condition(
        tweets_collector.get_raw_list(),
        lambda tweet: tweet.user_name == username
    )
