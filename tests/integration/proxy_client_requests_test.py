import stweet as st


def test_using_proxy_client():
    phrase = '#koronawirus'
    search_tweets_task = st.SearchTweetsTask(
        all_words=phrase,
        tweets_limit=200
    )
    # Default network
    proxy_client = st.ProxyClientRequests(None)
    tweets_collector = st.CollectorTweetOutput()
    result = st.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_outputs=[tweets_collector],
        web_client=proxy_client
    ).run()
    scrapped_tweets = tweets_collector.get_scrapped_tweets()
    assert isinstance(result, st.SearchTweetsResult)
    assert result.downloaded_count == len(scrapped_tweets)
    assert result.downloaded_count > 0
    assert all([phrase in it.full_text for it in scrapped_tweets if phrase in it.full_text]) is True
