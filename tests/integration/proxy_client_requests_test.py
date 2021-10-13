import stweet as st
from stweet.twitter_api.twitter_auth_web_client_interceptor import TwitterAuthWebClientInterceptor


def test_using_proxy_client():
    task = st.SearchTweetsTask(
        all_words='#covid19',
        tweets_limit=200
    )
    proxy_client = st.RequestsWebClient(
        proxy=st.RequestsWebClientProxyConfig(
            http_proxy='http://localhost:3128',
            https_proxy='http://localhost:3128'
        ),
        interceptors=[TwitterAuthWebClientInterceptor()]
    )
    tweets_collector = st.CollectorTweetOutput()
    result = st.TweetSearchRunner(
        search_tweets_task=task,
        tweet_outputs=[tweets_collector],
        web_client=proxy_client
    ).run()
    scrapped_tweets = tweets_collector.get_raw_list()
    assert isinstance(result, st.SearchTweetsResult)
    assert len(scrapped_tweets) == task.tweets_limit
