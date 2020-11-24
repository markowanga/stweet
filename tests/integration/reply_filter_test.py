import stweet as st


def test_search_as_replay():
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_count=500,
        replies_filter=st.RepliesFilter.ONLY_REPLIES
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector, st.PrintTweetOutput()]
    ).run()
    assert all([
        len(it.in_reply_to_status_id_str + it.in_reply_to_user_id_str) > 0
        for it in tweets_collector.get_scrapped_tweets()
    ]) is True


def test_search_as_not_replay():
    search_tweets_task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_count=500,
        replies_filter=st.RepliesFilter.ONLY_ORIGINAL
    )
    tweets_collector = st.CollectorTweetOutput()
    st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector, st.PrintTweetOutput()]
    ).run()
    assert all([
        len(it.in_reply_to_status_id_str + it.in_reply_to_user_id_str) == 0
        for it in tweets_collector.get_scrapped_tweets()
    ]) is True
