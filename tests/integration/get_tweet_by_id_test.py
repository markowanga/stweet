from typing import List, Tuple

import stweet as st
from stweet import RequestsWebClient
from stweet.http_request import RequestDetails, RequestResponse
from stweet.http_request.interceptor.logging_requests_web_client_interceptor import \
    LoggingRequestsWebClientInterceptor
from stweet.twitter_api.twitter_auth_web_client_interceptor import TwitterAuthWebClientInterceptor

_TWITTER_JSON_NO_TWEETS = '{"globalObjects":{"tweets":{},"users":{},"moments":{},"cards":{},"places":{}' \
                          ',"media":{},"broadcasts":{},"topics":{},"lists":{}},"timeline":{"id":"search' \
                          '-6749090958448035293","instructions":[{"addEntries":{"entries":[{"entryId":"' \
                          'sq-cursor-top","sortIndex":"999999999","content":{"operation":{"cursor":{"va' \
                          'lue":"refresh:thGAVUV0VFVBYBFgESNQAVACUAERXsiHoVgIl6GAdERUZBVUxUFQAVABUBFQAV' \
                          'AAA=","cursorType":"Top"}}}},{"entryId":"sq-cursor-bottom","sortIndex":"0","' \
                          'content":{"operation":{"cursor":{"value":"scroll:thGAVUV0VFVBYBFgESNQAVACUAE' \
                          'RXsiHoVgIl6GAdERUZBVUxUFQAVABUBFQAVAAA=","cursorType":"Bottom"}}}}]}}]}}'


class CustomAdapter(RequestsWebClient):

    def __init__(self, override: List[Tuple[str, RequestResponse]]):
        super().__init__()
        self.override = override

    def run_request(self, params: RequestDetails) -> RequestResponse:
        filtered = [it for it in self.override if it[0] == params.url]
        if len(filtered) > 0:
            return filtered[0][1]
        else:
            return super().run_request(params)


def test_get_tweets_by_ids():
    tweets_ids = ['1337071849772093442', '1337067073051238400']
    task = st.TweetsByIdTask(tweets_ids)
    collect_output = st.CollectorTweetOutput()
    result = st.TweetsByIdRunner(task, [collect_output],
                                 web_client=RequestsWebClient(
                                      interceptors=[LoggingRequestsWebClientInterceptor(),
                                                    TwitterAuthWebClientInterceptor()])).run()
    scrapped_tweets_ids = [it.id_str for it in collect_output.get_raw_list()]
    assert result.downloaded_count == 1
    assert len(collect_output.get_raw_list()) == 1
    assert len(result.tweet_ids_not_scrapped) == 1


def test_get_not_existing_tweet():
    tweets_ids = ['1337071849772093442']
    task = st.TweetsByIdTask(tweets_ids)
    collect_output = st.CollectorTweetOutput()
    result = st.TweetsByIdRunner(
        task,
        [collect_output],
        web_client=CustomAdapter(
            [('https://cdn.syndication.twimg.com/tweet', RequestResponse(404, ''))])
    ).run()
    assert result.downloaded_count == 0
    assert len(result.tweet_ids_not_scrapped) == 1


def test_get_not_existing_tweet_in_twitter():
    tweets_ids = ['1337071849772093442']
    task = st.TweetsByIdTask(tweets_ids)
    collect_output = st.CollectorTweetOutput()
    result = st.TweetsByIdRunner(
        task,
        [collect_output],
        web_client=CustomAdapter(
            [('https://api.twitter.com/2/search/adaptive.json',
              RequestResponse(200, _TWITTER_JSON_NO_TWEETS))]
        )
    ).run()
    assert result.downloaded_count == 0
    assert len(result.tweet_ids_not_scrapped) == 1


test_get_tweets_by_ids()
