import sys
from io import StringIO

import stweet as st
from stweet.http_request import HttpMethod
from stweet.http_request.interceptor.logging_requests_web_client_interceptor import LoggingRequestsWebClientInterceptor
from stweet.http_request.interceptor.params_response_log_web_client_interceptor import \
    ParamsResponseLogWebClientInterceptor
from stweet.twitter_api.twitter_api_requests import TwitterApiRequests


def get_example_request_details() -> st.http_request.RequestDetails:
    return st.http_request.RequestDetails(
        http_method=HttpMethod.GET,
        url='https://api.github.com/events',
        params=dict({}),
        headers=dict({}),
        timeout=200
    )


def start_redirect_output() -> StringIO:
    captured_output = StringIO()
    sys.stdout = captured_output
    sys.stderr = captured_output
    return captured_output


def stop_redirect_output():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


def test_logging_requests_web_client_interceptor():
    captured_output = start_redirect_output()
    request = TwitterApiRequests().get_guest_token_request_details()
    st.RequestsWebClient(interceptors=[LoggingRequestsWebClientInterceptor()]).run_request(request)
    stop_redirect_output()
    content = captured_output.getvalue()
    assert "send: b'POST /1.1/guest/activate.json HTTP/1.1" in content


def test_params_response_log_web_client_interceptor():
    captured_output = start_redirect_output()
    st.RequestsWebClient(interceptors=[ParamsResponseLogWebClientInterceptor()]).run_request(
        TwitterApiRequests().get_guest_token_request_details())
    stop_redirect_output()
    content = captured_output.getvalue()
    assert "RequestDetails(" in content
    assert "RequestResponse(" in content
