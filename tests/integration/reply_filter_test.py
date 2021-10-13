import stweet as st
from tests.test_util import tweet_list_assert_condition


def test_search_as_replay():
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_limit=500,
        replies_filter=st.RepliesFilter.ONLY_REPLIES
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    tweet_list_assert_condition(
        tweets_collector.get_raw_list(),
        lambda tweet: len(tweet.in_reply_to_status_id_str + tweet.in_reply_to_user_id_str) > 0
    )


def test_search_as_not_replay():
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_limit=500,
        replies_filter=st.RepliesFilter.ONLY_ORIGINAL
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector]
    ).run()
    tweet_list_assert_condition(
        tweets_collector.get_raw_list(),
        lambda tweet: len(tweet.in_reply_to_status_id_str + tweet.in_reply_to_user_id_str) == 0
    )
