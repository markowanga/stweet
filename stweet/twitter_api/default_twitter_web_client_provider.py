"""DefaultTwitterWebClientProvider class."""
from .twitter_auth_web_client_interceptor import TwitterAuthWebClientInterceptor
from ..http_request import WebClient, RequestsWebClient


class DefaultTwitterWebClientProvider:
    """DefaultTwitterWebClientProvider class."""

    def get_web_client(self) -> WebClient:
        """Method returns default WebClient."""
        return RequestsWebClient(interceptors=[TwitterAuthWebClientInterceptor()])
