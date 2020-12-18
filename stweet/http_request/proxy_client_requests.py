"""Request search_runner class."""

import requests
from typing import Dict, Any, Optional

from . import WebClient
from .request_details import RequestDetails
from .request_response import RequestResponse


class ProxyClientRequests(WebClient):
    """Request search_runner class with proxy support. Implementation based on requests library."""

    def __init__(self, proxies: Dict[str, str], options: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.proxies = proxies
        self.options = options

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
