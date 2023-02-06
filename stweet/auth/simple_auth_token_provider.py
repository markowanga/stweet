"""Util to process access token to Twitter api."""

import json
import time
from json import JSONDecodeError
from typing import Callable, Optional

from ..exceptions import RefreshTokenException
from ..exceptions.too_many_requests_exception import TooManyRequestsException
from ..http_request import WebClient
from ..twitter_api.twitter_api_requests import TwitterApiRequests
from .auth_token_provider import AuthTokenProvider
from .fail_strategy.auth_fail_strategy import AuthFailStrategy
from .fail_strategy.wait_auth_fail_strategy import WaitAuthFailStrategy

_TIMEOUT = 20
_URL = 'https://api.twitter.com/1.1/guest/activate.json'


def _run_retrying_for_string(
        stop_max_ms: int,
        on_except_function: Callable[[], None],
        catch_predicate: Callable[[Exception], bool],
        call_function: Callable[[], str]
) -> str:
    def current_milli_time():
        return round(time.time() * 1000)

    first_error_time = -1
    result = None
    while result is None:
        try:
            result = call_function()
        except Exception as e:
            if first_error_time == -1:
                first_error_time = current_milli_time()
            time_from_first_error = current_milli_time() - first_error_time
            is_time_over = time_from_first_error > stop_max_ms
            if not catch_predicate(e) or is_time_over:
                raise e
            on_except_function()
    return result


class SimpleAuthTokenProvider(AuthTokenProvider):
    """Class to manage Twitter token api."""

    auth_fail_strategy: AuthFailStrategy
    stop_max_delay_on_too_many_requests_exception: int

    def __init__(
            self,
            auth_fail_strategy: Optional[AuthFailStrategy] = None,
            stop_max_delay_on_too_many_requests_exception: int = 40 * 60 * 1000
    ):
        """Constructor of SimpleAuthTokenProvider, can override default retries time."""
        self.auth_fail_strategy = auth_fail_strategy
        if self.auth_fail_strategy is None:
            self.auth_fail_strategy = WaitAuthFailStrategy(60 * 1000)
        self.stop_max_delay_on_too_many_requests_exception = \
            stop_max_delay_on_too_many_requests_exception

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
        return _run_retrying_for_string(
            stop_max_ms=self.stop_max_delay_on_too_many_requests_exception,
            on_except_function=self.auth_fail_strategy.run_strategy,
            catch_predicate=lambda e: isinstance(e, TooManyRequestsException),
            call_function=simple_get_new_token
        )
