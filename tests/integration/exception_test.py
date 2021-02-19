import pytest

import stweet as st
from stweet import WebClient
from stweet.auth import SimpleAuthTokenProvider
from stweet.exceptions import RefreshTokenException, ScrapBatchBadResponse
from stweet.exceptions.too_many_requests_exception import TooManyRequestsException
from stweet.http_request import RequestResponse
from stweet.twitter_api.twitter_auth_web_client_interceptor import TwitterAuthWebClientInterceptor
from tests.mock_web_client import MockWebClient


def get_client_with_default_response(response: RequestResponse = RequestResponse(None, None)) -> WebClient:
    return MockWebClient(
        default_response=response,
        interceptors=[TwitterAuthWebClientInterceptor()]
    )


def test_get_simple_auth_token_with_incorrect_response_1():
    with pytest.raises(RefreshTokenException):
        SimpleAuthTokenProvider().get_new_token(get_client_with_default_response(RequestResponse(400, None)))


def test_get_auth_token_with_incorrect_response_2():
    with pytest.raises(TooManyRequestsException):
        SimpleAuthTokenProvider(50, 150).get_new_token(get_client_with_default_response(RequestResponse(429, None)))


def test_get_auth_token_with_incorrect_response_3():
    with pytest.raises(RefreshTokenException):
        SimpleAuthTokenProvider().get_new_token(get_client_with_default_response(RequestResponse(200, '{}')))


def test_get_auth_token_with_incorrect_response_4():
    with pytest.raises(RefreshTokenException):
        SimpleAuthTokenProvider().get_new_token(get_client_with_default_response(RequestResponse(200, 'LALA')))


def test_runner_exceptions():
    class TokenExpiryExceptionWebClient(st.WebClient):

        count_dict = dict({
            'https://api.twitter.com/2/search/adaptive.json': 0,
            'https://api.twitter.com/1.1/guest/activate.json': 0
        })

        def run_clear_request(self, params: st.http_request.RequestDetails) -> st.http_request.RequestResponse:
            self.count_dict[params.url] = self.count_dict[params.url] + 1
            if params.url == 'https://api.twitter.com/2/search/adaptive.json':
                if self.count_dict[params.url] == 1:
                    return st.http_request.RequestResponse(429, None)
                else:
                    return st.http_request.RequestResponse(400, '')
            else:
                return st.http_request.RequestResponse(200, '{"guest_token":"1350356785648062465"}')

    with pytest.raises(ScrapBatchBadResponse):
        search_tweets_task = st.SearchTweetsTask(
            all_words='#koronawirus'
        )
        st.TweetSearchRunner(
            search_tweets_task=search_tweets_task,
            tweet_outputs=[],
            web_client=TokenExpiryExceptionWebClient(interceptors=[TwitterAuthWebClientInterceptor()]),
        ).run()


def test_get_not_existing_user():
    task = st.GetUsersTask(['fcbewkjdsncvjwkfs'])
    result = st.GetUsersRunner(task, []).run()
    assert result.users_count == 0
