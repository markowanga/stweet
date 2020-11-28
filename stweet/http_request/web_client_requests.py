"""Request runner class."""

import requests

from . import WebClient
from .request_details import RequestDetails
from .request_response import RequestResponse


class WebClientRequests(WebClient):
    """Request runner class. Implementation based on requests library."""

    def run_request(self, params: RequestDetails) -> RequestResponse:
        """Main method to run request using requests package."""
        session = requests.Session()
        response = session.request(
            method=params.http_method.name,
            url=params.url,
            params=params.params,
            headers=params.headers,
            timeout=params.timeout
        )
        return RequestResponse(response.status_code, response.text)
