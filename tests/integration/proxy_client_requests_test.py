import stweet as st


def test_using_proxy_client():
    task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_limit=200
    )
    proxy_client = st.RequestsWebClient(
        st.RequestsWebClientProxyConfig(
            http_proxy='http://localhost:3128',
            https_proxy='http://localhost:3128'
        )
    )
    tweets_collector = st.CollectorTweetOutput()
    result = st.TweetSearchRunner(
        search_tweets_task=task,
        tweet_outputs=[tweets_collector],
        web_client=proxy_client
    ).run()
    scrapped_tweets = tweets_collector.get_scrapped_tweets()
    assert isinstance(result, st.SearchTweetsResult)
    assert len(scrapped_tweets) == task.tweets_limit
