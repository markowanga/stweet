"""Request search_runner class with proxy support."""

import requests

from . import WebClient
from .request_details import RequestDetails
from .request_response import RequestResponse


class ProxyRequestsWebClient(WebClient):
    """Request search_runner class with proxy support. Implementation based on requests library."""

    def __init__(self, http_proxy: str, https_proxy: str, verify: bool = False):
        """Constructor to create a web client."""
        super().__init__()
        self.proxies = dict({
            'http': http_proxy,
            'https': https_proxy
        })
        self.options = dict({
            'verify': verify
        })

    def run_request(self, params: RequestDetails) -> RequestResponse:
        """Main method to run request using requests package."""
        session = requests.Session()
        response = session.request(
            method=params.http_method.name,
            url=params.url,
            params=params.params,
            headers=params.headers,
            timeout=params.timeout,
            proxies=self.proxies,
            **self.options
        )
        return RequestResponse(response.status_code, response.text)
