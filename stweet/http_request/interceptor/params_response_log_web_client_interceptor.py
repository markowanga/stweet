"""Class of ParamsResponseLogWebClientInterceptor."""
import threading
from typing import List

from .. import RequestDetails, RequestResponse, RequestsWebClient, WebClient


class ParamsResponseLogWebClientInterceptor(WebClient.WebClientInterceptor):
    """Class of ParamsResponseLogWebClientInterceptor.

    Interceptor log input params and out response.
    """

    _counter: int
    _lock: threading.Lock

    def __init__(self):
        """Constructor of ParamsResponseLogWebClientInterceptor."""
        self._value = 0
        self._lock = threading.Lock()

    def increment(self) -> int:
        """Thread safe increment. Returns old value."""
        with self._lock:
            to_return = self._value
            self._value += 1
            return to_return

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
        index = self.increment()
        if is_to_log:
            print(f'{index} -- {requests_details}')
        to_return = self.get_response(requests_details, next_interceptors, web_client)
        if is_to_log:
            print(f'{index} -- {to_return}')
        return to_return
