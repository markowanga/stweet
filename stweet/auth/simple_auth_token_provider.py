"""Util to process access token to Twitter api."""

import json
from json import JSONDecodeError

from .auth_token_provider import AuthTokenProvider, AuthTokenProviderFactory
from ..exceptions import RefreshTokenException
from ..http_request import HttpMethod
from ..http_request import RequestDetails, WebClient

_retries = 5
_timeout = 20
_url = 'https://api.twitter.com/1.1/guest/activate.json'
_auth_token = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81' \
              'IUq16cHjhLTvJu4FA33AGWWjCpTnA'


class SimpleAuthTokenProvider(AuthTokenProvider):
    """Class to manage Twitter token api."""

    web_client: WebClient

    def __init__(self, web_client: WebClient):
        """Constructor of TokenRequest."""
        self.web_client = web_client
        return

    def _request_for_response_body(self):
        """Method from Twint."""
        token_request_details = RequestDetails(HttpMethod.POST, _url, {'Authorization': _auth_token}, dict(), _timeout)
        token_response = self.web_client.run_request(token_request_details)
        if token_response.is_success():
            return token_response.text
        else:
            raise RefreshTokenException('Error during request for token')

    def get_new_token(self) -> str:
        """Method to get refreshed token. In case of error raise RefreshTokenException."""
        try:
            token_html = self._request_for_response_body()
            return json.loads(token_html)['guest_token']
        except JSONDecodeError:
            raise RefreshTokenException('Error during request for token')


class SimpleAuthTokenProviderFactory(AuthTokenProviderFactory):
    """Provider of SimpleAuthTokenProviderFactory."""

    def create(self, web_client: WebClient) -> AuthTokenProvider:
        """Method to create SimpleAuthTokenProvider from web_client."""
        return SimpleAuthTokenProvider(web_client)
