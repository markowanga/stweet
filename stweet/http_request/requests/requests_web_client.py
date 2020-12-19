"""Request search_runner class."""
from typing import Optional, Dict

import requests

from .requests_web_client_proxy_config import RequestsWebClientProxyConfig
from ..request_details import RequestDetails
from ..request_response import RequestResponse
from ..web_client import WebClient


class RequestsWebClient(WebClient):
    """Request search_runner class. Implementation based on requests library."""

    proxy: Optional[RequestsWebClientProxyConfig]
    verify: bool

    def __init__(
            self,
            proxy: Optional[RequestsWebClientProxyConfig] = None,
            verify: bool = True
    ):
        """Constructor of RequestsWebClient."""
        self.proxy = proxy
        self.verify = verify

    def run_request(self, params: RequestDetails) -> RequestResponse:
        """Main method to run request using requests package."""
        session = requests.Session()
        response = session.request(
            method=params.http_method.name,
            url=params.url,
            params=params.params,
            headers=params.headers,
            timeout=params.timeout,
            proxies=self._get_proxy(),
            verify=self.verify
        )
        return RequestResponse(response.status_code, response.text)

    def _get_proxy(self) -> Dict[str, str]:
        return None if self.proxy is None else dict({
            'http': self.proxy.http_proxy,
            'https': self.proxy.https_proxy,
        })
