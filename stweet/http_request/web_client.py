"""Web client abstract class."""
from abc import abstractmethod

from .request_details import RequestDetails
from .request_response import RequestResponse


class WebClient:
    """Web client abstract class."""

    @abstractmethod
    def run_request(self, params: RequestDetails) -> RequestResponse:
        """Abstract method to run request."""
