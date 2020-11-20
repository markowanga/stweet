"""Request runner class."""
import requests

from .request_details import RequestDetails
from .request_response import RequestResponse


class RequestRunner:
    """Request runner class. Implementation based on requests library."""

    @staticmethod
    def run_request(params: RequestDetails) -> RequestResponse:
        """Main method to run request."""
        session = requests.Session()
        response = session.get(
            url=params.url,
            params=params.params,
            headers=params.headers,
            timeout=params.timeout
        )
        return RequestResponse(response.status_code, response.text)
