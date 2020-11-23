"""Util to process access token to Twitter api."""

import re

from ..exceptions import RefreshTokenException
from ..http_request import RequestDetails, WebClient
from ..http_request.http_method import HttpMethod

_retries = 5
_timeout = 20
_url = 'https://twitter.com'


class TwitterAuthTokenProvider:
    """Class to manage Twitter token api."""

    web_client: WebClient

    def __init__(self, web_client: WebClient):
        """Constructor of TokenRequest."""
        self.web_client = web_client
        return

    def _request_for_response_body(self):
        """Method from Twint."""
        token_request_details = RequestDetails(HttpMethod.GET, _url, dict(), dict(), _timeout)
        token_response = self.web_client.run_request(token_request_details)
        if token_response.is_success():
            return token_response.text
        else:
            raise RefreshTokenException('Error during request for token')

    def refresh(self) -> str:
        """Method to get refreshed token. In case of error raise RefreshTokenException."""
        token_html = self._request_for_response_body()
        match = re.search(r'\("gt=(\d+);', token_html)
        if match:
            return str(match.group(1))
        else:
            print('Could not find the Guest token in HTML')
            print(token_html)
            raise RefreshTokenException('Could not find the Guest token in HTML')
