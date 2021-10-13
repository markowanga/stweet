"""Util to process access token to Twitter api."""

import json
from json import JSONDecodeError

from retrying import retry

from .auth_token_provider import AuthTokenProvider
from ..exceptions import RefreshTokenException
from ..exceptions.too_many_requests_exception import TooManyRequestsException
from ..http_request import WebClient
from ..twitter_api.twitter_api_requests import TwitterApiRequests

_TIMEOUT = 20
_URL = 'https://api.twitter.com/1.1/guest/activate.json'


class SimpleAuthTokenProvider(AuthTokenProvider):
    """Class to manage Twitter token api."""

    wait_fixed_on_too_many_requests_exception: int
    stop_max_delay_on_too_many_requests_exception: int

    def __init__(
            self,
            wait_fixed_on_too_many_requests_exception: int = 60 * 1000,
            stop_max_delay_on_too_many_requests_exception: int = 40 * 60 * 1000
    ):
        """Constructor of SimpleAuthTokenProvider, can override default retries time."""
        self.wait_fixed_on_too_many_requests_exception = wait_fixed_on_too_many_requests_exception
        self.stop_max_delay_on_too_many_requests_exception = stop_max_delay_on_too_many_requests_exception

    def _request_for_response_body(self, web_client: WebClient):
        """Method from Twint."""
        token_request_details = TwitterApiRequests().get_guest_token_request_details()
        token_response = web_client.run_request(token_request_details)
        if token_response.is_success():
            return token_response.text
        else:
            raise RefreshTokenException(f'Error during request for token -- {token_response}')

    def get_new_token(self, web_client: WebClient) -> str:
        """Method to get refreshed token. In case of error raise RefreshTokenException."""

        def simple_get_new_token() -> str:
            try:
                token_html = self._request_for_response_body(web_client)
                return json.loads(token_html)['guest_token']
            except JSONDecodeError:
                raise RefreshTokenException('Error during request for token')
            except KeyError:
                raise RefreshTokenException('Error during request for token')

        # by this https://github.com/rholder/retrying/issues/70#issuecomment-313129305
        return retry(
            wait_fixed=self.wait_fixed_on_too_many_requests_exception,
            stop_max_delay=self.stop_max_delay_on_too_many_requests_exception,
            retry_on_exception=lambda e: isinstance(e, TooManyRequestsException)
        )(simple_get_new_token)()
