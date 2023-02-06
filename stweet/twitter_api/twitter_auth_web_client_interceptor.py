"""Class of TwitterAuthWebClientInterceptor."""
from threading import Lock
from typing import List, Optional

from stweet.auth import AuthTokenProvider, SimpleAuthTokenProvider
from stweet.exceptions.too_many_requests_exception import \
    TooManyRequestsException
from stweet.http_request import (RequestDetails, RequestResponse,
                                 RequestsWebClient, WebClient)

_AUTH_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4p' \
              'uTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
_MAX_TRIES = 5


class TwitterAuthWebClientInterceptor(WebClient.WebClientInterceptor):
    """Class of TwitterAuthWebClientInterceptor.

    Interceptor allows to simple manage auth requests.
    """

    _current_token: Optional[str]
    _auth_token_provider: AuthTokenProvider
    _quest_token_lock: Lock

    def __init__(
            self,
            init_auth_token: Optional[str] = None,
            auth_token_provider: Optional[AuthTokenProvider] = None
    ):
        """Constructor of AuthWebClientInterceptor."""
        self._current_token = init_auth_token
        self._auth_token_provider = auth_token_provider \
            if auth_token_provider is not None \
            else SimpleAuthTokenProvider()
        self._quest_token_lock = Lock()

    def _add_auth_token(self, request_details: RequestDetails):
        request_details.headers['Authorization'] = _AUTH_TOKEN

    def _add_guest_token(self, request_details: RequestDetails, web_client: WebClient):
        if self._current_token is None:
            self._call_for_new_auth_request(web_client)
        request_details.headers['x-guest-token'] = self._current_token

    def _is_auth_token_to_add(self, request_details: RequestDetails) -> bool:
        return 'http://api.twitter.com' in request_details.url \
               or 'https://api.twitter.com' in request_details.url \
               or 'https://twitter.com/i/api' in request_details.url

    def _is_guest_token_to_add(self, request_details: RequestDetails) -> bool:
        if 'https://twitter.com/i/api/graphql/' in request_details.url:
            return True
        is_guest_request = '/1.1/guest/activate.json' in request_details.url
        return self._is_auth_token_to_add(request_details) and not is_guest_request

    def _call_for_new_auth_request(self, web_client: WebClient):
        old_token = self._current_token
        with self._quest_token_lock:
            if old_token == self._current_token:
                self._current_token = self._auth_token_provider.get_new_token(web_client)

    def intercept(
            self,
            requests_details: RequestDetails,
            next_interceptors: List[WebClient.WebClientInterceptor],
            web_client: RequestsWebClient
    ) -> RequestResponse:
        """Method intercepts request. It manage with auth headers."""
        need_guest_token = self._is_guest_token_to_add(requests_details)
        if self._is_auth_token_to_add(requests_details):
            self._add_auth_token(requests_details)

        if need_guest_token:
            self._add_guest_token(requests_details, web_client)

        response: Optional[RequestResponse] = None
        tries_counter = 0

        while tries_counter < _MAX_TRIES and (response is None or response.is_429()):
            if need_guest_token and response is not None:
                self._call_for_new_auth_request(web_client)
                self._add_guest_token(requests_details, web_client)
            response = self.get_response(requests_details, next_interceptors, web_client)
            tries_counter = tries_counter + 1

        if response.is_429():
            raise TooManyRequestsException(requests_details.url)

        return response
