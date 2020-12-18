"""Request search_runner class with proxy support."""

import requests
from typing import Dict, Any, Optional

from . import WebClient
from .request_details import RequestDetails
from .request_response import RequestResponse
from stweet.exceptions.invalid_requests_param_exception import InvalidRequestsParamException


class ProxyClientRequests(WebClient):
    """Request search_runner class with proxy support. Implementation based on requests library."""

    def __init__(self, proxies: Dict[str, str], options: Optional[Dict[str, Any]] = None):
        """Constructor to create a web client."""
        super().__init__()
        self.proxies = proxies
        self.options = dict() if options is None else options
        if self.proxies is not None and not isinstance(self.proxies, dict):
            raise InvalidRequestsParamException("Proxies must be a dict or None to use default network.")
        if not isinstance(self.options, dict):
            raise InvalidRequestsParamException("Options must be a dict.")

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
