"""Util to process access token to Twitter api."""

import json
from json import JSONDecodeError

from retrying import retry

from .auth_token_provider import AuthTokenProvider
from ..exceptions import RefreshTokenException
from ..exceptions.too_many_requests_exception import TooManyRequestsException
from ..http_request import HttpMethod
from ..http_request import RequestDetails, WebClient

_TIMEOUT = 20
_URL = 'https://api.twitter.com/1.1/guest/activate.json'


class SimpleAuthTokenProvider(AuthTokenProvider):
    """Class to manage Twitter token api."""

    def _get_auth_request_details(self) -> RequestDetails:
        return RequestDetails(HttpMethod.POST, _URL, dict(), dict(), _TIMEOUT)

    def _request_for_response_body(self, web_client: WebClient):
        """Method from Twint."""
        token_request_details = self._get_auth_request_details()
        token_response = web_client.run_request(token_request_details)
        if token_response.is_success():
            return token_response.text
        else:
            raise RefreshTokenException(f'Error during request for token -- {token_response}')

    @retry(
        wait_fixed=60 * 1000,
        stop_max_delay=40 * 60 * 1000,
        retry_on_exception=lambda e: isinstance(e, TooManyRequestsException)
    )
    def get_new_token(self, web_client: WebClient) -> str:
        """Method to get refreshed token. In case of error raise RefreshTokenException."""
        try:
            token_html = self._request_for_response_body(web_client)
            return json.loads(token_html)['guest_token']
        except JSONDecodeError:
            raise RefreshTokenException('Error during request for token')
