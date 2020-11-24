import stweet as st
from tests.test_util import to_base_text


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


def test_return_tweets_from_user():
    username = 'realDonaldTrump'
    search_tweets_task = st.SearchTweetsTask(
        from_username=username,
        tweets_count=100
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    assert all([
        it.user_name == username
        for it in tweets_collector.get_scrapped_tweets()
    ]) is True
