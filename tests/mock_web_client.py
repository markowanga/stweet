from typing import Optional, List, Dict

import stweet as st
from stweet import WebClient
from stweet.http_request import RequestDetails, RequestResponse


class MockWebClient(st.WebClient):
    responses: Optional[Dict[str, RequestResponse]]
    default_response: Optional[RequestResponse]

    def __init__(
            self,
            interceptors: Optional[List[WebClient.WebClientInterceptor]] = None,
            default_response: Optional[RequestResponse] = None,
            responses: Optional[Dict[str, RequestResponse]] = None
    ):
        super().__init__(interceptors)
        self.responses = responses
        self.default_response = default_response

    def run_clear_request(self, params: RequestDetails) -> RequestResponse:
        if self.responses is not None and params.url in self.responses.keys():
            return self.responses[params.url]
        elif self.default_response is not None:
            return self.default_response
        else:
            raise Exception('no value to return')
