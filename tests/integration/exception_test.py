import pytest

import stweet as st
from stweet.auth import SimpleAuthTokenProvider
from stweet.exceptions import RefreshTokenException, ScrapBatchBadResponse
from stweet.http_request import RequestDetails, RequestResponse
from tests.mock_web_client import MockWebClient


def test_get_auth_token_with_incorrect_response_1():
    with pytest.raises(RefreshTokenException):
        SimpleAuthTokenProvider(MockWebClient(None, None)).get_new_token()


def test_get_simple_auth_token_with_incorrect_response_1():
    with pytest.raises(RefreshTokenException):
        SimpleAuthTokenProvider(MockWebClient(None, None)).get_new_token()


def test_get_auth_token_with_incorrect_response_2():
    with pytest.raises(RefreshTokenException):
        SimpleAuthTokenProvider(MockWebClient(400, 'None')).get_new_token()


def test_get_auth_token_with_incorrect_response_3():
    with pytest.raises(RefreshTokenException):
        SimpleAuthTokenProvider(MockWebClient(200, 'None')).get_new_token()


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
            web_client=TokenExpiryExceptionWebClient(None),
            auth_token_provider_factory=st.auth.SimpleAuthTokenProviderFactory()

        ).run()


def test_get_not_existing_user():
    task = st.GetUsersTask(['fcbewkjdsncvjwkfs'])
    result = st.GetUsersRunner(task, []).run()
    assert result.users_count == 0
