"""Abstract class for get guest auth token."""
from abc import abstractmethod

from ..http_request.web_client import WebClient


class AuthTokenProvider:
    """Abstract class for get guest auth token."""

    @abstractmethod
    def get_new_token(self) -> str:
        """Method returns new token."""


class AuthTokenProviderFactory:
    """Provider of AuthTokenProvider."""

    @abstractmethod
    def create(self, web_client: WebClient) -> AuthTokenProvider:
        """Method to create AuthTokenProvider from web_client."""
