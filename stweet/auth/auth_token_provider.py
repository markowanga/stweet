"""Abstract class for get guest auth token."""
from abc import abstractmethod

from ..http_request.web_client import WebClient


class AuthTokenProvider:
    """Abstract class for get guest auth token."""

    @abstractmethod
    def get_new_token(self, web_client: WebClient) -> str:
        """Method returns new token."""
