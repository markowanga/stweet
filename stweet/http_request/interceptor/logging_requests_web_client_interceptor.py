"""Class of LoggingRequestsWebClientInterceptor."""
import logging
from http.client import HTTPConnection
from typing import List

from .. import RequestDetails, RequestResponse, RequestsWebClient, WebClient


class LoggingRequestsWebClientInterceptor(WebClient.WebClientInterceptor):
    """Class of LoggingRequestsWebClientInterceptor."""

    @staticmethod
    def _debug_requests_on():
        """Switches on logging of the requests module."""
        HTTPConnection.debuglevel = 1

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    @staticmethod
    def _debug_requests_off():
        """Switches off logging of the requests module, might be some side-effects."""
        HTTPConnection.debuglevel = 0

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.WARNING)
        root_logger.handlers = []
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.NOTSET)
        requests_log.propagate = False

    def logs_to_show(self, params: RequestDetails) -> bool:
        """Method to decide that show logs of request.

        Method can be overridden and then the logs will be filtered – example by request url.
        """
        return True

    def intercept(
            self,
            requests_details: RequestDetails,
            next_interceptors: List[WebClient.WebClientInterceptor],
            web_client: RequestsWebClient
    ) -> RequestResponse:
        """Method show logs when predicate is true. Uses static field so it can be problem with concurrency."""
        is_to_log = self.logs_to_show(requests_details)
        if is_to_log:
            LoggingRequestsWebClientInterceptor._debug_requests_on()
        to_return = self.get_response(requests_details, next_interceptors, web_client)
        if is_to_log:
            LoggingRequestsWebClientInterceptor._debug_requests_off()
        return to_return
