from .twitter_auth_web_client_interceptor import TwitterAuthWebClientInterceptor
from ..http_request import WebClient, RequestsWebClient


class DefaultTwitterWebClientProvider:

    def get_web_client(self) -> WebClient:
        return RequestsWebClient(interceptors=[TwitterAuthWebClientInterceptor()])
