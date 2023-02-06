"""Web client abstract class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from .request_details import RequestDetails
from .request_response import RequestResponse


def _run_request_with_interceptors(
        requests_details: RequestDetails,
        next_interceptors: List[WebClient.WebClientInterceptor],
        web_client: WebClient
) -> RequestResponse:
    return next_interceptors[0].intercept(requests_details, next_interceptors[1:], web_client) if len(
        next_interceptors) > 0 else web_client.run_clear_request(requests_details)


class WebClient:
    """Web client abstract class."""

    _interceptors: List[WebClientInterceptor]

    def __init__(self, interceptors: Optional[List[WebClientInterceptor]]):
        """Base constructor of class."""
        self._interceptors = [] if interceptors is None else interceptors

    def run_request(self, requests_details: RequestDetails) -> RequestResponse:
        """Method process the request. Method wrap request with interceptors."""
        return _run_request_with_interceptors(requests_details, self._interceptors, self)

    @abstractmethod
    def run_clear_request(self, params: RequestDetails) -> RequestResponse:
        """Abstract method to run only the request."""

    class WebClientInterceptor(ABC):
        """Abstract class of web client interceptor."""

        @staticmethod
        def get_response(
                requests_details: RequestDetails,
                next_interceptors: List[WebClient.WebClientInterceptor],
                web_client: WebClient
        ) -> RequestResponse:
            """Method process request. If any interceptor passes method wrap request with this."""
            return _run_request_with_interceptors(requests_details, next_interceptors, web_client)

        @abstractmethod
        def intercept(
                self,
                requests_details: RequestDetails,
                next_interceptors: List[WebClient.WebClientInterceptor],
                web_client: WebClient
        ) -> RequestResponse:
            """Interceptor method of request.

            Method need to call WebClientInterceptor.get_response to process request by next interceptors
            and client.
            """
